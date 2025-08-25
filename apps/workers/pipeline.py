# apps/workers/pipeline.py (only the publish() function changed)
from .celery_app import app
from libs.common.fetch import fetch_url
from libs.common.parse import parse_html, parse_pdf
from libs.common.storage import put_bytes, get_sha256, S3_BUCKET_RAW, guess_ext
from libs.severity.score import score_severity

from sqlalchemy import select
from libs.models.session import SessionLocal
from sqlalchemy import select
from apps.pdfgen.jurisdiction_digest import render_and_upload_digest
from libs.common.storage import S3_BUCKET_PDF
from libs.models.db import Rule

@app.task
def discover(jurisdiction: str) -> list[str]:
    seeds = {
        "CA": ["https://www.dir.ca.gov/dlse/faq_mealperiods.htm"],
        "NYC": [
            "https://www.nyc.gov/site/dca/workers/workersrights/fastfood-retail-workers.page",
            "https://www.nyc.gov/site/dca/businesses/fairworkweek-deductions-laws-employers.page",
        ],
    }
    return seeds.get(jurisdiction, [])

@app.task
def fetch(url: str) -> dict:
    """
    Returns a dict: {"url":..., "content": bytes, "sha256": "...", "s3_key": "raw-docs/..."}
    """
    content = fetch_url(url)
    sha = get_sha256(content)
    # derive key: raw-docs/<sha>.<ext>
    ext = ".pdf" if url.lower().endswith(".pdf") else (guess_ext(None, url) or ".html")
    key = f"{sha[:2]}/{sha}{ext}"
    put_bytes(S3_BUCKET_RAW, key, content, content_type=("application/pdf" if ext==".pdf" else "text/html; charset=utf-8"))
    return {"url": url, "content": content, "sha256": sha, "s3_key": key}

@app.task
def parse(url: str, payload: dict) -> str:
    content: bytes = payload.get("content") or b""
    if not content:
        return ""
    if url.lower().endswith(".pdf"):
        return parse_pdf(content)
    return parse_html(content)

@app.task
def normalize(jurisdiction: str, family: str, text: str, raw_meta: dict | None = None) -> dict:
    rule = {
        "id": f"rule://US/{jurisdiction}/{family}/demo",
        "jurisdiction": {"level":"state" if len(jurisdiction)==2 else "city", "name": jurisdiction, "parent": None},
        "rule_family": family,
        "obligations": [],
        "penalties_premiums": [],
        "citations": [],
        "provenance": {"source": "demo"},
    }
    if raw_meta:
        rule["provenance"].update({
            "raw_url": raw_meta.get("url"),
            "raw_sha256": raw_meta.get("sha256"),
            "raw_s3_key": raw_meta.get("s3_key"),
        })
    rule["severity"] = score_severity(rule)
    return rule

@app.task
def verify(rule: dict) -> dict:
    rule.setdefault("citations", []).append({"url":"https://example.org","section":"§demo","quote":"example","confidence":0.5})
    return rule

@app.task
def publish(rule: dict) -> dict:
    # UPSERT into Postgres
    db = SessionLocal()
    try:
        rid = rule["id"]
        existing = db.get(Rule, rid)
        if existing:
            existing.family = rule.get("rule_family") or rule.get("family")
            existing.jurisdiction = rule.get("jurisdiction")
            existing.obligations = rule.get("obligations", [])
            existing.penalties = rule.get("penalties_premiums", [])
            existing.citations = rule.get("citations", [])
            existing.provenance = rule.get("provenance", {})
            existing.effective = rule.get("effective")
            existing.severity = rule.get("severity", {})
        else:
            db.add(Rule(
                id=rid,
                family=rule.get("rule_family") or rule.get("family"),
                jurisdiction=rule.get("jurisdiction"),
                obligations=rule.get("obligations", []),
                penalties=rule.get("penalties_premiums", []),
                citations=rule.get("citations", []),
                provenance=rule.get("provenance", {}),
                effective=rule.get("effective"),
                severity=rule.get("severity", {}),
            ))
        db.commit()
    finally:
        db.close()
    return rule

@app.task
def generate_jurisdiction_pdf(jcode: str) -> dict:
    db = SessionLocal()
    try:
        from libs.models.db import Rule
        rows = db.execute(select(Rule)).scalars().all()
        rules = []
        for r in rows:
            j = (r.jurisdiction or {})
            if j.get("name") == jcode or j.get("parent") == jcode:
                rules.append({
                    "rule_family": r.family,
                    "severity": r.severity,
                    "provenance": r.provenance,
                    "obligations": r.obligations,
                })
        key = render_and_upload_digest(jcode, rules)
        return {"ok": True, "s3_key": key, "bucket": S3_BUCKET_PDF, "count": len(rules)}
    finally:
        db.close()

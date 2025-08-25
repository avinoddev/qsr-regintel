# apps/pdfgen/jurisdiction_digest.py
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import tempfile, os
from libs.common.storage import put_bytes, S3_BUCKET_PDF

def render_digest(path: str, title: str, sections: list[tuple[str,str]]):
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER
    c.setTitle(title)
    y = height - 72
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, title)
    y -= 24
    c.setFont("Helvetica", 10)
    for heading, body in sections:
        if y < 100:
            c.showPage(); y = height - 72; c.setFont("Helvetica", 10)
        c.drawString(72, y, heading); y -= 14
        for line in body.splitlines():
            if y < 72:
                c.showPage(); y = height - 72; c.setFont("Helvetica", 10)
            c.drawString(90, y, line[:100]); y -= 12
        y -= 8
    c.showPage()
    c.save()

def render_and_upload_digest(jcode: str, rules: list[dict]) -> str:
    title = f"QSR Regulatory Digest — {jcode}"
    # crude section text from rules for demo
    sections = []
    for r in rules:
        fam = r.get("rule_family","?")
        sev = r.get("severity",{}).get("level","?")
        prov = r.get("provenance",{})
        src = prov.get("raw_url") or "n/a"
        sections.append(
            (f"{fam} — Severity: {sev}", f"Source: {src}\nObligations: {len(r.get('obligations',[]))}\n")
        )
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        path = tmp.name
    try:
        render_digest(path, title, sections)
        with open(path, "rb") as f:
            key = f"jurisdiction/{jcode}/latest.pdf"
            put_bytes(S3_BUCKET_PDF, key, f.read(), "application/pdf")
        return key
    finally:
        try: os.remove(path)
        except Exception: pass

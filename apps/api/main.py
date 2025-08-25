# apps/api/main.py
import os
from fastapi import FastAPI, Query, Body, Depends
from typing import Optional
from fastapi_pagination import add_pagination, paginate, Page
from sqlalchemy import select
from sqlalchemy.orm import Session

from libs.models.db import Base, Rule
from libs.models.session import engine, SessionLocal
from libs.common.storage import (
    ensure_bucket, S3_BUCKET_RAW, S3_BUCKET_PDF,
    presign_get_public   # use public signer so host is baked correctly
)

app = FastAPI(title="QSR-RegIntel API", version="0.2.1")

# --- DB lifecycle ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)
    ensure_bucket(S3_BUCKET_RAW)
    ensure_bucket(S3_BUCKET_PDF)

# --- Helpers ---
def rule_row_to_dict(r: Rule) -> dict:
    return {
        "id": r.id,
        "jurisdiction": r.jurisdiction,
        "rule_family": r.family,
        "obligations": r.obligations,
        "penalties_premiums": r.penalties,
        "citations": r.citations,
        "provenance": r.provenance,
        "effective": r.effective,
        "severity": r.severity,
        "created_at": str(r.created_at),
        "updated_at": str(r.updated_at),
    }

# --- Endpoints ---
@app.get("/rules", response_model=Page[dict])
def list_rules(
    jurisdiction: Optional[str] = None,
    family: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db),
):
    rows = db.execute(select(Rule)).scalars().all()
    if jurisdiction:
        j = jurisdiction.strip()
        rows = [r for r in rows if isinstance(r.jurisdiction, dict)
                and (r.jurisdiction.get("name") == j or r.jurisdiction.get("parent") == j)]
    if family:
        rows = [r for r in rows if getattr(r, "family", None) == family]
    if severity:
        lv = {x.strip() for x in severity.split(",")}
        rows = [r for r in rows if isinstance(r.severity, dict) and r.severity.get("level") in lv]
    return paginate([rule_row_to_dict(r) for r in rows])

# Single, correct PDF route
@app.get("/pdf/jurisdictions/{code}/latest")
def get_pdf(code: str):
    key = f"jurisdiction/{code}/latest.pdf"
    url = presign_get_public(S3_BUCKET_PDF, key, expires=3600)
    return {"pdf_url": url, "s3_key": key}

add_pagination(app)

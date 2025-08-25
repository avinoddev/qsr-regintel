
from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Text, JSON, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

class Base(DeclarativeBase):
    pass

def gen_uuid():
    return str(uuid.uuid4())

class RawDocument(Base):
    __tablename__ = "raw_documents"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    url: Mapped[str] = mapped_column(String, nullable=False)
    mime: Mapped[str] = mapped_column(String, nullable=False)
    sha256: Mapped[str] = mapped_column(String, nullable=False)
    bytes: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    retrieved_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

class ParsedSection(Base):
    __tablename__ = "parsed_sections"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    doc_id: Mapped[str] = mapped_column(String, ForeignKey("raw_documents.id"))
    section_id: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    page_spans: Mapped[dict] = mapped_column(JSON)

class Rule(Base):
    __tablename__ = "rules"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    family: Mapped[str] = mapped_column(String, index=True)
    jurisdiction: Mapped[dict] = mapped_column(JSON)
    obligations: Mapped[dict] = mapped_column(JSON)
    penalties: Mapped[dict] = mapped_column(JSON)
    severity: Mapped[dict] = mapped_column(JSON)
    citations: Mapped[list] = mapped_column(JSON)
    provenance: Mapped[dict] = mapped_column(JSON)
    effective: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

class Change(Base):
    __tablename__ = "changes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    rule_id: Mapped[str] = mapped_column(String, ForeignKey("rules.id"))
    change_type: Mapped[str] = mapped_column(String)
    diff: Mapped[dict] = mapped_column(JSON)
    changed_on: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

class RenderedPdf(Base):
    __tablename__ = "rendered_pdfs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    scope: Mapped[dict] = mapped_column(JSON)  # {"type":"jurisdiction","value":"CA"} or {"type":"family","value":"predictive_scheduling"}
    s3_key: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

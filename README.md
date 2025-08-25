# QSR-RegIntel 🏪⚖️

**Automated Regulatory Intelligence Platform for Quick Service Restaurants (QSRs)**

This project is an AI-driven system that continuously monitors, extracts, and normalizes labor regulations (federal, state, and local) that impact QSR operators.  
It provides both **machine-readable outputs** (JSON, API) and **human-friendly digests** (PDFs) with severity scoring and review workflows.

---

## 🚀 Features

- **Multi-agent pipeline**: discover → fetch → parse → normalize → verify → publish.
- **Persistence**: all rules stored in Postgres with full provenance (citations, raw source, severity).
- **Artifact storage**: raw HTML/PDF and generated digests stored in MinIO (S3-compatible).
- **PDF digests**: auto-generated jurisdiction reports, downloadable via presigned URLs.
- **Verifier v1**: section + quote binding with confidence scoring; low-confidence items pushed into a review queue.
- **API**: REST endpoints for querying rules, downloading PDFs, and managing review items.

---
- `libs/severity` — Severity scoring heuristics
- `libs/common` — Utilities (fetching, parsing, OCR, robots, hashing, change-diff)
- `infra` — Docker Compose, Alembic migrations, config
- `tests` — Unit tests and gold set harness
>>>>>>> 4439708 (feat: MVP infra, DB persistence, MinIO storage, PDFs, Verifier v1)

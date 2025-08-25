<<<<<<< HEAD
# qsr-regintel
=======

# QSR-RegIntel — Regulatory Intelligence Platform (Starter)

This repository is a production-ready starter for an AI-driven regulatory intelligence platform
targeting U.S. labor regulations for Quick Service Restaurants (QSRs). It implements the
multi-agent pipeline described in your spec: Discovery → Fetch → Parse → Normalize → Verify →
Score Severity → Change-Watch → Publish.

> Generated on 2025-08-25T04:31:46.657002Z

## Quick Start (Local)

1) Install Docker and Docker Compose.
2) `make up` (starts Postgres, Redis, MinIO, API, Workers).
3) Visit `http://localhost:8080/docs` for API (FastAPI).
4) `make seed` to seed baseline config (jurisdictions, families).
5) `make ingest CA` to run a California demo ingestion job (stub extractor).

## Services

- **API**: FastAPI at `:8080`
- **Workers**: Celery workers executing pipeline jobs
- **Queue**: Redis (broker + result backend)
- **DB**: Postgres
- **Blob store**: MinIO (S3 compatible) for raw documents and rendered PDFs

## Folders
- `apps/api` — REST API
- `apps/workers` — Celery tasks for pipeline stages
- `apps/pdfgen` — Jurisdiction/Category digest rendering
- `libs/models` — Pydantic + SQLAlchemy models
- `libs/rules` — Specialists per rule family
- `libs/severity` — Severity scoring heuristics
- `libs/common` — Utilities (fetching, parsing, OCR, robots, hashing, change-diff)
- `infra` — Docker Compose, Alembic migrations, config
- `tests` — Unit tests and gold set harness
>>>>>>> 4439708 (feat: MVP infra, DB persistence, MinIO storage, PDFs, Verifier v1)

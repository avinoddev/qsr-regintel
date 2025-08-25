.PHONY: up down logs api workers db shell seed migrate ingest ingest-%

COMPOSE = docker compose -f infra/docker-compose.yml

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f --tail=200

api:
	$(COMPOSE) exec api bash

workers:
	$(COMPOSE) exec workers bash

db:
	$(COMPOSE) exec db psql -U regintel -d regintel

shell:
	$(COMPOSE) exec api python -i

seed:
	$(COMPOSE) exec api python -m infra.seeds.seed_config

migrate:
	$(COMPOSE) exec api alembic upgrade head

ingest:
	$(COMPOSE) exec api python -m apps.workers.cli run-demo

ingest-%:
	$(COMPOSE) exec api python -m apps.workers.cli run-demo --jurisdiction $*

pdf-%:
	$(COMPOSE) exec api python -c "from apps.workers.pipeline import generate_jurisdiction_pdf; print(generate_jurisdiction_pdf.run('$*'))"

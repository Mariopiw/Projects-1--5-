# Intelligent Operations Automation Platform

![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Workflow](https://img.shields.io/badge/Automation-Human%20Reviewed-168A67)
[![CI](https://github.com/Mariopiw/Projects-1--5-/actions/workflows/ci.yml/badge.svg)](https://github.com/Mariopiw/Projects-1--5-/actions/workflows/ci.yml)

A **reference operations platform** for reconciling business records, detecting discrepancies, triaging exceptions, and automating controlled legacy-system interactions. Designed as a portfolio project in Python backend engineering, workflow automation, and operational reliability.

The included AI triage pathway defaults to a **deterministic mock**: the repository is reproducible without a paid LLM API. Human oversight remains essential for sensitive operational decisions.

## Architecture

~~~mermaid
flowchart LR
  E["ERP / WMS records"] --> API["FastAPI + JWT/RBAC"]
  API --> DB[("PostgreSQL")]
  DB --> R["Reconciliation engine"]
  R --> X["Exception cases"]
  X --> T["Mock AI / policy triage"]
  T --> H["Human review"]
  H --> Q["Redis / Celery job queue"]
  Q --> P["Playwright legacy portal adapter"]
  P --> A["Audit trail"]
~~~

## Core components

| Component | What it demonstrates |
|---|---|
| FastAPI + Pydantic | Typed API endpoints and request validation |
| PostgreSQL + Alembic | Durable records, migrations and transactional integrity |
| Reconciliation engine | Detecting mismatches and creating exception workflows |
| AI-assisted triage | Interpretable, mock-first prioritization with human oversight |
| JWT and role checks | Differentiated operator access controls |
| Celery + Redis | Asynchronous tasks and scheduled automation |
| Playwright integration | Browser automation when no suitable API is available |
| Mock portal | Safe, synthetic end-to-end legacy-system test target |
| Audit records | Traceability for operational actions |
| pytest + CI | Automated regression checks and quality gates |

The default mock portal is designed for local testing. Do not point automated browser actions at a real third-party portal without authorization and an explicit change-control plan.

## Getting started — local Docker Compose lab

**Requirements:** Docker, Docker Compose, sufficient RAM/storage, and available local ports 8000 and 9000.

~~~bash
git clone https://github.com/Mariopiw/Projects-1--5-.git
cd Projects-1--5-

cp .env.example .env

# Edit .env before startup:
# - JWT_SECRET and WEBHOOK_SHARED_SECRET
# - Database, portal and other demo passwords
# - Keep AI_PROVIDER=mock for the first run
docker compose up --build
~~~

After the services become healthy:

- **FastAPI docs:** http://localhost:8000/docs
- **Mock legacy portal:** http://localhost:9000

Use synthetic order or inventory records in your tests; never upload confidential operations data to a portfolio environment.

**Important:** the bundled Docker database and mock portal use development credentials. Local demos are not hardened production deployments. Confirm your Docker port bindings and firewall rules before making the stack available outside your laptop.

## Unit tests, linting and seed fixtures

Python 3.12+:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

pytest --cov=app --cov-report=term-missing
ruff check .
~~~

After configuring a working database, seed demo data via:

~~~bash
python -m scripts.seed
~~~

Test modules cover API behavior, reconciliation logic, triage rules and exception workflows. The repo documents further failure drills in [docs/TESTING.md](docs/TESTING.md); planned tests should not be confused with completed evidence.

## Repository structure

~~~text
app/                FastAPI routes, security, DB models and business services
app/integrations/   Legacy-portal adapter
app/tasks/          Redis/Celery asynchronous jobs
mock_portal/        Local authorized browser-automation target
migrations/         Database schema evolution
scripts/            Synthetic data seeding
tests/              Automated test suite
docs/               Architecture, runbook, threat model and ADRs
docker-compose.yml  Local service orchestration
Makefile            Developer commands
~~~

## Engineering decisions and limits

- **API-first:** favor explicit APIs; resort to browser automation when no supported API exists.
- **Human control:** significant decisions and legacy-system updates should be reviewed.
- **Operational visibility:** audit traces, categorized exceptions and reconciliation workflows.
- **Failure awareness:** database outages, task retries, portal timeouts, duplicate events and state recovery require testing.
- **Production limitations:** not independently audited, not a production-certified ERP/WMS integration, and not guaranteed compliant with any regulatory regime.

## Technical documentation

[Architecture](docs/ARCHITECTURE.md) · [Runbook](docs/RUNBOOK.md) · [Security](docs/SECURITY.md) · [Testing](docs/TESTING.md) · [Architecture decisions](docs/adr/) · [Source code](app/)

## License

See the existing [LICENSE](LICENSE). 

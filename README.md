# Intelligent Operations Automation Platform

A production-style portfolio project demonstrating how a junior+/early-mid Python Automation & Integration Engineer can reconcile operational data, detect exceptions, apply controlled AI-assisted triage, orchestrate workflows, and bridge a legacy browser-only system.

## What this project demonstrates

- Python 3.12
- FastAPI + Pydantic
- SQLAlchemy + PostgreSQL
- OAuth2 password flow + JWT + RBAC
- Reconciliation and exception domain logic
- Human-reviewed AI-assisted triage (mock provider by default)
- Celery + Redis asynchronous jobs and scheduled escalation
- Playwright legacy-system integration
- Idempotent/duplicate-safe database constraints
- Audit logging
- Docker Compose
- Alembic migrations
- pytest + coverage
- GitHub Actions CI
- Architecture, security, testing, runbook, and ADR documentation

## Business scenario

An ERP says an order should contain 10 units. A warehouse reports 7. The platform detects the discrepancy, creates an exception, classifies severity, provides a triage recommendation, allows an operator to acknowledge/resolve it, and can launch a background automation job to verify the order in a mock legacy portal.

## Architecture

```text
ERP/WMS input
    |
    v
 FastAPI --------> PostgreSQL
    |                 |
    v                 v
Reconciliation --> Exception
                       |
                       v
                 Triage policy
                       |
                  Human review
                       |
                       v
                 Celery / Redis
                       |
                       v
                   Playwright
                       |
                       v
                 Legacy portal
                       |
                       v
                    Audit log
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Quick start (Linux Mint)

```bash
git clone https://github.com/Mariopiw/Projects-1--5-.git
cd Projects-1--5-
cp .env.example .env
openssl rand -hex 32
docker compose up --build
```

Open:
- API docs: http://localhost:8000/docs
- Mock legacy portal: http://localhost:9000

### Demo credentials
Local demo only:
- `viewer / viewer123`
- `operator / operator123`
- `admin / admin123`

## Tests
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest --cov=app --cov-report=term-missing
```

## Engineering principles

1. Business rules are independent of HTTP/UI layers.
2. API/database integrations are preferred over browser automation.
3. AI is decision support, not an unrestricted actuator.
4. High-impact actions require human review.
5. Duplicate requests must not create duplicate business effects.
6. Background work is retried with bounded exponential backoff.
7. Operational actions are auditable.
8. Failures should degrade safely rather than silently corrupt state.

## Security
Read [docs/SECURITY.md](docs/SECURITY.md) before using this outside a local portfolio environment.

## License
MIT

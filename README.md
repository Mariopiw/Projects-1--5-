# Intelligent Operations Automation Platform

A reference platform for reconciling operational records, flagging discrepancies, supporting human-reviewed AI triage, and automating legacy-system checks.

## Key features

- FastAPI and PostgreSQL for operational records and exceptions
- Reconciliation logic and role-based access control
- AI-assisted recommendations with human review
- Celery/Redis jobs and Playwright integration with a mock legacy portal
- Audit logging and automated tests

## Quick start

Requires Docker Compose. Review `.env` and replace demo credentials before using outside an isolated local environment.

```bash
git clone https://github.com/Mariopiw/Projects-1--5-.git
cd Projects-1--5-
cp .env.example .env
docker compose up --build
```

API documentation: http://localhost:8000/docs

Mock legacy portal: http://localhost:9000

## Tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest --cov=app --cov-report=term-missing
```

**Scope:** Local portfolio/reference application. Read `docs/SECURITY.md` before deploying or handling real data. Architecture details: `docs/ARCHITECTURE.md`.

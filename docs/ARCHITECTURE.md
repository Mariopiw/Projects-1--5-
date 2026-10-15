# Architecture

## Flow

```text
ERP/WMS data
   |
   v
FastAPI -> PostgreSQL -> Reconciliation Engine -> Exception
                                      |
                                      v
                               Triage Decision
                                      |
                           Human acknowledgement/review
                                      |
                                      v
                              Celery/Redis worker
                                      |
                                      v
                              Playwright adapter
                                      |
                                      v
                               Legacy portal
                                      |
                                      v
                                 Audit trail
```

## Design choices

- **PostgreSQL** for transactions, constraints, and reporting.
- **FastAPI/Pydantic** for typed APIs and validation.
- **Celery/Redis** for background work and scheduled escalation.
- **Playwright** only for systems without a usable API.
- **Human-in-the-loop** before sensitive operational changes.
- **Audit logging** for traceability.

The default AI implementation is deliberately deterministic/mock-based so the repository runs without paid external services. Replace `app/services/triage.py` with a provider adapter only after adding evaluation, privacy controls, and fallbacks.

# Local Runbook

## Start
```bash
cp .env.example .env
docker compose up --build
```

Open API docs at `http://localhost:8000/docs`.

Demo users seeded automatically:
- viewer / viewer123
- operator / operator123
- admin / admin123

Change these immediately outside a local demo.

## Basic demo
1. Authenticate at `/auth/token`.
2. `POST /orders`.
3. `POST /warehouse-records`.
4. `POST /reconciliation/run`.
5. `GET /exceptions`.
6. Acknowledge or resolve an exception.
7. Create an automation job referencing the exception.
8. `POST /jobs/{id}/run`.
9. Inspect jobs and audit trail.

## Stop
```bash
docker compose down
```

# Testing Strategy

## Unit
- Reconciliation rules
- Severity thresholds
- Triage policy
- State transitions

## API/integration
- Authentication and RBAC
- Duplicate handling
- Reconciliation persistence
- Exception listing and lifecycle

## Failure drills to add
1. PostgreSQL unavailable
2. Redis unavailable
3. Portal timeout
4. Invalid selector
5. Invalid credentials
6. Duplicate job/event
7. AI provider unavailable

Run:
```bash
pytest --cov=app --cov-report=term-missing
```

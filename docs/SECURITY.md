# Security Notes

This is a portfolio-grade reference implementation, not a production certification.

## Implemented
- Password hashing with `pwdlib` recommended algorithm.
- Signed JWT bearer authentication.
- Role checks (`viewer`, `operator`, `admin`).
- Secrets supplied through environment variables.
- ORM-based SQL access and input validation.
- Human review for AI-assisted decisions.
- Audit events for operational actions.

## Before production
- Replace bootstrap demo credentials.
- Use a managed identity provider (e.g. Entra ID/Auth0/Keycloak).
- Store secrets in a cloud secret manager.
- Add TLS termination, rate limiting, CSRF considerations for browser clients, and security headers.
- Add webhook signature verification for external event ingestion.
- Add dependency scanning and container scanning.
- Define retention/minimization rules for personal or regulated data.

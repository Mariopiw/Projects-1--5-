# ADR-002: Browser automation only when APIs are unavailable

## Context
UI automation is more brittle than direct system integration.

## Decision
Prefer REST/database integrations. Use Playwright only for the mock legacy portal or real systems where authorized APIs do not exist.

## Consequences
The browser adapter is isolated so it can be replaced by UiPath, Power Automate, or a future API without rewriting business logic.

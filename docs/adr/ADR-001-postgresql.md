# ADR-001: PostgreSQL

## Context
The platform requires transactions, uniqueness constraints, audit queries, and reliable persistence.

## Decision
Use PostgreSQL as the production-style relational store. SQLite remains useful for local unit tests.

## Consequences
More setup than flat files, but stronger consistency and realistic deployment practices.

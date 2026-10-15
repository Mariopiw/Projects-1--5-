from fastapi import FastAPI

from app.routers import auth, exceptions, jobs, orders

app = FastAPI(
    title="Intelligent Operations Automation Platform",
    version="0.1.0",
    description="Portfolio-grade platform for reconciliation, exception workflows, AI-assisted triage, and legacy portal automation.",
)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(exceptions.router)
app.include_router(jobs.router)


@app.get("/health")
def health():
    return {"status": "ok"}

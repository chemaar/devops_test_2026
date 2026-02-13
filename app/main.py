from fastapi import FastAPI

from app.api.routes import tickets, users
from app.core.config import settings

app = FastAPI(title=settings.api_title, version=settings.api_version)

app.include_router(users.router)
app.include_router(tickets.router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

from fastapi import FastAPI

from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Track monthly spending and learn professional FastAPI patterns.",
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Finance Tracker API", "docs": "/docs"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.db import Base, SessionLocal
from app.main import app


def test_create_transaction_and_monthly_summary(tmp_path: Path) -> None:
    database_path = tmp_path / "test_finance_tracker.db"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )

    previous_bind = SessionLocal.kw["bind"]
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        client = TestClient(app)

        payload = {
            "date": "2026-05-01",
            "description": "Coffee",
            "category": "food",
            "amount": "4.50",
            "is_subscription": False,
        }

        created = client.post("/api/transactions", json=payload)
        assert created.status_code == 201
        assert created.json()["category"] == "food"

        listed = client.get("/api/transactions")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        summary = client.get(
            "/api/reports/monthly-summary",
            params={"year": 2026, "month": 5},
        )
        assert summary.status_code == 200
        assert summary.json()["total"] == "4.50"
    finally:
        SessionLocal.configure(bind=previous_bind)
        engine.dispose()

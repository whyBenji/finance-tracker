from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.transaction import MonthlySummary
from app.services.transactions import get_monthly_summary

router = APIRouter(prefix="/reports", tags=["reports"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/monthly-summary", response_model=MonthlySummary)
def monthly_summary_endpoint(
    db: DbSession,
    year: Annotated[int, Query(ge=2000, le=2100)],
    month: Annotated[int, Query(ge=1, le=12)],
) -> MonthlySummary:
    return get_monthly_summary(db, year=year, month=month)

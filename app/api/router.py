from fastapi import APIRouter

from app.api.routes.reports import router as reports_router
from app.api.routes.transactions import router as transactions_router

api_router = APIRouter()
api_router.include_router(transactions_router)
api_router.include_router(reports_router)

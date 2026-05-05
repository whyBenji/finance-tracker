from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.services.transactions import (
    create_transaction,
    delete_transaction,
    get_transaction,
    list_transactions,
    update_transaction,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction_endpoint(payload: TransactionCreate, db: DbSession) -> TransactionRead:
    transaction = create_transaction(db, payload)
    return TransactionRead.model_validate(transaction)


@router.get("", response_model=list[TransactionRead])
def list_transactions_endpoint(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[TransactionRead]:
    transactions = list_transactions(db, skip=skip, limit=limit)
    return [TransactionRead.model_validate(transaction) for transaction in transactions]


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction_endpoint(transaction_id: int, db: DbSession) -> TransactionRead:
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return TransactionRead.model_validate(transaction)


@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction_endpoint(
    transaction_id: int,
    payload: TransactionUpdate,
    db: DbSession,
) -> TransactionRead:
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    updated = update_transaction(db, transaction, payload)
    return TransactionRead.model_validate(updated)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_endpoint(transaction_id: int, db: DbSession) -> Response:
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    delete_transaction(db, transaction)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import MonthlySummary, TransactionCreate, TransactionUpdate


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def list_transactions(db: Session, skip: int = 0, limit: int = 100) -> list[Transaction]:
    statement = select(Transaction).order_by(Transaction.date.desc(), Transaction.id.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement))


def get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    return db.get(Transaction, transaction_id)


def update_transaction(
    db: Session,
    transaction: Transaction,
    payload: TransactionUpdate,
) -> Transaction:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction) -> None:
    db.delete(transaction)
    db.commit()


def get_monthly_summary(db: Session, year: int, month: int) -> MonthlySummary:
    start_date = date(year, month, 1)
    end_date = date(year + (month // 12), (month % 12) + 1, 1)

    total_statement = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
        Transaction.date >= start_date,
        Transaction.date < end_date,
    )
    total = Decimal(db.scalar(total_statement) or 0)

    category_statement = (
        select(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
        )
        .where(
            Transaction.date >= start_date,
            Transaction.date < end_date,
        )
        .group_by(Transaction.category)
        .order_by(Transaction.category.asc())
    )

    by_category = [
        {"category": row.category, "total": Decimal(row.total)}
        for row in db.execute(category_statement)
    ]

    return MonthlySummary(
        year=year,
        month=month,
        total=total,
        by_category=by_category,
    )

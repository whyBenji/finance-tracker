import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionBase(BaseModel):
    date: dt.date
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    is_subscription: bool = False

    @field_validator("description", "category")
    @classmethod
    def strip_strings(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    date: dt.date | None = None
    description: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    is_subscription: bool | None = None

    @field_validator("description", "category")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class TransactionRead(TransactionBase):
    id: int
    created_at: dt.datetime
    updated_at: dt.datetime

    model_config = ConfigDict(from_attributes=True)


class CategorySummary(BaseModel):
    category: str
    total: Decimal


class MonthlySummary(BaseModel):
    year: int
    month: int
    total: Decimal
    by_category: list[CategorySummary]

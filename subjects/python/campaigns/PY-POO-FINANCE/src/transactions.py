from pydantic import BaseModel, field_validator
from datetime import date, datetime


class Transaction(BaseModel):
    id: str
    amount: float
    date: date
    currency: str
    description: str = ""
    category: str = ""


class Income(Transaction):
    @field_validator("amount")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Amount must be positive")
        return v


class Expense(Transaction):
    @field_validator("amount")
    @classmethod
    def ensure_positive(cls, v: float) -> float:
        return abs(v)


def create_transaction(raw_data: dict) -> Transaction:
    parse_date = datetime.strptime(raw_data["date"], "%Y-%m-%d").date()
    txn_type = str(raw_data.get("type", "")).strip().lower()

    if txn_type == "income":
        return Income(
            id=raw_data["id"],
            date=parse_date,
            amount=float(raw_data["amount"]),
            currency=raw_data["currency"],
            description=raw_data.get("description", ""),
            category=raw_data.get("category", ""),
        )
    elif txn_type == "expense":
        return Expense(
            id=raw_data["id"],
            date=parse_date,
            amount=float(raw_data["amount"]),
            currency=raw_data["currency"],
            description=raw_data.get("description", ""),
            category=raw_data.get("category", ""),
        )
    else:
        raise ValueError("Unknown type by data input")


def map_all(raw_data: list[dict]) -> list[Transaction]:
    return [create_transaction(raw) for raw in raw_data]
# result=[]
# for raw in raw_data
#   log = create_transaction(raw)
#   result.append(log)
# return result

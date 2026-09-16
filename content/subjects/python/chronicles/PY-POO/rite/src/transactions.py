from abc import abstractmethod, ABC


class Transaction(ABC):
    def __init__(self, amount: float, date: str, category: str):
        self.amount = amount
        self.date = date
        self.category = category

    @abstractmethod
    def get_signed_amount(self) -> float:
        pass


class Income(Transaction):
    def get_signed_amount(self):
        return abs(self.amount)


class Expense(Transaction):
    def get_signed_amount(self):
        return -abs(self.amount)


def build_transactions(raw_data: list[dict]) -> list[Transaction]:
    transactions = []
    for row in raw_data:
        if row["type"] == "Income":
            transactions.append(
                Income(float(row["amount"]), row["date"], row["category"]))
        elif row["type"] == "Expense":
            transactions.append(
                Expense(float(row["amount"]), row["date"], row["category"]))
    return transactions

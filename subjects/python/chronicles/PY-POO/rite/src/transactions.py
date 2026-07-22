from abc import abstractmethod, ABC


class Transaction(ABC):
    def __init__(self, amount: float, date: str):
        self.amount = amount
        self.date = date

    @abstractmethod
    def get_signed_amount(self) -> float:
        pass


class Income(Transaction):
    def get_signed_amount(self):
        return abs(self.amount)


class Expense(Transaction):
    def get_signed_amount(self):
        return -abs(self.amount)


class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner
        self.balance = initial_balance

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount: float):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False


if __name__ == "__main__":
    account = BankAccount("Ander", 100.0)
    print(account.balance)

    account.deposit(50.0)
    print(account.balance)
    account.withdraw(30.0)
    print(account.balance)
    account.withdraw(500.0)
    print(account.balance)

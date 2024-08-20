"""
Create a Python class representing a bank account. The class should support methods for depositing, withdrawing, and checking the balance.
"""


class BankAccount:
    def __init__(self, balance: float = 0.0) -> None:
        self.balance = balance

    def deposit(self, amount: float) -> float:
        if amount > 0:
            self.balance += amount
            return self.balance

    def withdraw(self, amount: float) -> float:
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                return self.balance

    def check_balance(self) -> float:
        return self.balance


# Example usage
account = BankAccount()
account.deposit(100)
account.withdraw(30)
print(account.check_balance())  # Output: 70

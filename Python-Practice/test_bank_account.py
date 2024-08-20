import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount()

    def test_initial_balance(self):
        self.assertEqual(self.account.check_balance(), 0)

    def test_deposit(self):
        self.assertEqual(self.account.deposit(50.0), 50.0)

    def test_withdraw(self):
        self.account.deposit(50.0)
        self.assertEqual(self.account.withdraw(25), 25.0)

    def test_withdraw_insufficient_fund(self):
        self.account.deposit(50)
        self.assertEqual(self.account.withdraw(70), None)

    def test_withdraw_negative_amount(self):
        self.account.deposit(50)
        self.assertEqual(self.account.withdraw(-70), None)


if __name__ == "__main__":
    unittest.main()

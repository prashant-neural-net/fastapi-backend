import pytest
from app.cal import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account(init: int = 50):
    return BankAccount(init)

@pytest.mark.parametrize("num1, num2, expected",[
                            (1, 2, 3),
                            (2, 3, 5),
                            (7, 1, 8)
])

def test_add(num1: int, num2: int, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(10, 5) == 5

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5


def test_bank_default(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_bank_withdrawl(bank_account):
    bank_account.withdrawl(20)
    assert bank_account.balance == 30

def test_bank_innterest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposit, withdrawl, expected", [
    (100, 50, 50+50),
    (10, 10, 0+50),
    (90, 80, 10+50),
    (10, 90, -30)
])

def test_transaction(deposit, withdrawl, expected, bank_account):
    bank_account.deposit(deposit)
    bank_account.withdrawl(withdrawl)
    assert bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdrawl(1000)

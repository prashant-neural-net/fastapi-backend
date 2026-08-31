class InsufficientFunds(Exception):
    pass

def add(num1: int, num2: int):
    return num1+num2

def subtract(num1: int, num2: int):
    return num1-num2

def multiply(num1: int, num2: int):
    return num1*num2

def divide(num1: int, num2: int):
    return num1/num2


class BankAccount():
    def __init__(self, def_balance=0):
        self.balance = def_balance

    def deposit(self, amount):
        self.balance += amount
    
    def withdrawl(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("insufficient balance")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1
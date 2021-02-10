import random


class OutOfMoney(Exception):
    pass

class NotEnoughMoney(Exception):
    pass

class AbortInvestment(Exception):
    pass

class Strategy:
    def __str__(self):
        return self.__class__.__name__

class Impulsive(Strategy):
    @staticmethod
    def should_buy(balance, price, rent):
        return True

class Demanding(Strategy):
    @staticmethod
    def should_buy(balance, price, rent):
        return rent > 50

class Cautious(Strategy):
    @staticmethod
    def should_buy(balance, price, rent):
        return balance - price >= 80

class Gambler(Strategy):
    @staticmethod
    def should_buy(balance, price, rent):
        return random.choice((True, False))

STRATEGIES = (Impulsive(), Demanding(), Cautious(), Gambler())

class Player:
    def __init__(self, initial_balance, strategy=Impulsive()):
        self.balance = initial_balance
        self.strategy = strategy

    def pay(self, amount):
        if amount > self.balance:
            raise OutOfMoney(repr(self))

        self.balance -= amount
        return amount

    def receive(self, amount):
        self.balance += amount

    def invest(self, price, rent):
        if price > self.balance:
            raise NotEnoughMoney(f'{self!r} can not aford {price}.')

        if not self.strategy.should_buy(self.balance, price, rent):
            raise AbortInvestment(f'{self!r} aborted the investment.')

        return self.pay(price)

    def __str__(self):
        return str(self.strategy)

    @classmethod
    def from_strategies(cls, balance):
        return [cls(balance, strategy=s) for s in STRATEGIES]
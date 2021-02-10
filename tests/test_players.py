import pytest

from game.player import Player, OutOfMoney, NotEnoughMoney, Impulsive, AbortInvestment, Demanding, Cautious, Gambler


def test_init():
    p = Player(300)
    assert p
    assert p.balance == 300
    assert isinstance(p.strategy, Impulsive)

def test_pay():
    p = Player(10)
    assert p.pay(10) == 10
    assert p.balance == 0

def test_receive():
    p = Player(0)
    assert p.receive(10) is None
    assert p.balance == 10

def test_transfer():
    p1 = Player(10)
    p2 = Player(0)

    p2.receive(p1.pay(10))

    assert p1.balance == 0
    assert p2.balance == 10

def test_outofmoney():
    p = Player(0)

    with pytest.raises(OutOfMoney):
        p.pay(1)

def test_invest_impulsive():
    p = Player(100)
    assert p.invest(price=100, rent=10) == 100
    assert p.balance == 0

def test_invest_without_money():
    p = Player(10)

    with pytest.raises(NotEnoughMoney):
        p.invest(price=100, rent=10)

def test_invest_demanding():
    p = Player(100, strategy=Demanding())
    assert p.invest(price=100, rent=51) == 100
    assert p.balance == 0

def test_invest_demanding_abort():
    p = Player(100, strategy=Demanding())

    with pytest.raises(AbortInvestment):
        p.invest(price=100, rent=50)

def test_invest_cautious():
    p = Player(180, strategy=Cautious())
    assert p.invest(price=100, rent=10) == 100
    assert p.balance == 80

def test_invest_cautious_abort():
    p = Player(100, strategy=Cautious())

    with pytest.raises(AbortInvestment):
        p.invest(price=100, rent=10)

def test_invest_gambler(mocker):
    p = Player(100, strategy=Gambler())

    mocker.patch('random.choice', return_value=True)
    assert p.invest(price=100, rent=10) == 100
    assert p.balance == 0

def test_invest_gambler_abort(mocker):
    p = Player(100, strategy=Gambler())

    mocker.patch('random.choice', return_value=False)
    with pytest.raises(AbortInvestment):
        p.invest(price=100, rent=10)

def test_str():
    p = Player(0)
    assert str(p) == 'Impulsive'

def test_factory():
    players = Player.from_strategies(300)
    names = [str(p) for p in players]
    assert names == ['Impulsive', 'Demanding', 'Cautious', 'Gambler']
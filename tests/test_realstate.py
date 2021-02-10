import pytest

from game import RealState, Player


def test_init():
    r = RealState(50, 5)
    assert r.price == 50
    assert r.rent == 5
    assert r.owner is None

def test_not_has_owner():
    r = RealState(50, 5)
    assert r.has_owner() == False

def test_has_owner():
    p = Player(0)
    r = RealState(50, 5, owner=p)

    assert r.has_owner() == True

def test_owned_by():
    p1 = Player(0)
    p2 = Player(0)
    r1 = RealState(50, 5, owner=p1)

    assert r1.owner_is(p1) == True
    assert r1.owner_is(p2) == False

def test_foreclose():
    p = Player(0)
    r = RealState(50, 5, owner=p)

    r.foreclose()
    assert r.has_owner() == False

def test_sell():
    p = Player(100)
    r = RealState(50, 5)

    r.sell_to(p)

    assert r.owner_is(p)
    assert p.balance == 50

def test_sell_error():
    p1, p2 = Player(100), Player(0)
    r = RealState(50, 5, owner=p2)

    with pytest.raises(AssertionError):
        r.sell_to(p1)

def test_rent():
    p1, p2 = Player(0), Player(5)
    r = RealState(50, 5, owner=p1)

    r.rent_to(p2)
    assert p1.balance == 5
    assert p2.balance == 0

def test_rent_player_is_owner():
    p1 = Player(4)
    r1 = RealState(50, 5, owner=p1)

    r1.rent_to(p1)
    assert p1.balance == 4

def test_deal_sell():
    p1 = Player(100)
    r1 = RealState(50, 5)

    r1.deal(p1)
    assert r1.owner_is(p1)
    assert p1.balance == 50

def test_deal_rent():
    p1 = Player(100)
    p2 = Player(0)
    r2 = RealState(50, 5, owner=p2)

    r2.deal(p1)
    assert p2.balance == 5
    assert p1.balance == 95
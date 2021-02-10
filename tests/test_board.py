from game import Board, Player, RealState
from game.player import Demanding


def test_init():
    players = ()
    properties = ()
    b = Board(players, properties, bonus=1)

    assert b.players == {}
    assert b.properties == ()
    assert b.bonus == 1

def test_move():
    p = Player(0)
    r = RealState(100, 10)
    b = Board([p], [r])

    assert b.move(p, 1) == r

    assert b.move(p, 1) == r
    assert p.balance == 100

def test_len():
    r = RealState(100, 10)
    b = Board([], [r])

    assert len(b) == 1

def test_remove():
    p = Player(0)
    b = Board([p], [])

    b.remove(p)
    assert len(b.players) == 0

def test_turn_success():
    p = Player(300)
    r = RealState(100, 10)
    b = Board([p], [r])

    b.turn(p, 1)

    assert r.owner_is(p)
    assert p.balance == 200

def test_turn_abort_investment():
    p = Player(300, strategy=Demanding())
    r = RealState(100, 50)
    b = Board([p], [r])

    b.turn(p, 1)

    assert not r.has_owner()
    assert p.balance == 300

def test_turn_not_enough_money():
    p = Player(0)
    r = RealState(100, 50)
    b = Board([p], [r])

    b.turn(p, 1)

    assert not r.has_owner()
    assert p.balance == 0

def test_turn_out_of_money():
    p1 = Player(200)
    p2 = Player(49)
    r = RealState(100, 50, owner=p1)
    b = Board([p1, p2], [r])

    b.turn(p2, 1)

    assert p1 in b.players
    assert p2 not in b.players
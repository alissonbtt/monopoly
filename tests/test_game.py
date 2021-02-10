# Dá 300 dinheiros para cada jogador no início
# Finaliza quando tem apenas 1 jogador
# Encerra o jogo após 1000 rodadas.
from game import Player, RealState, Game


def test_init():
    players = Player.from_strategies(300)
    r = RealState(100, 10)
    g = Game(players, [r])

    assert [p.balance for p in players] == [300] * 4
    assert g.board

def test_leader():
    players = Player.from_strategies(0)
    players[1].receive(1)
    players[2].receive(2)
    players[3].receive(3)

    r = RealState(100, 10)
    g = Game(players, [r])

    assert g.leader == players[3]

def test_leader_tie():
    players = Player.from_strategies(0)
    r = RealState(100, 10)
    g = Game(players, [r])

    assert g.leader == players[0]

def test_dice():
    assert Game.dice() in range(1, 7)

def test_run_winner(mocker):
    p1 = Player(100)
    p2 = Player(0)
    r = RealState(100, 10)
    g = Game([p1, p2], [r])

    g.dice = lambda: 1

    winner = g.run()

    assert winner is p1

def test_run_tie():
    p1 = Player(100)
    p2 = Player(100)
    r = RealState(100, 10)
    g = Game([p1, p2], [r])

    g.dice = lambda: 1

    winner = g.run(998)

    assert winner is p2
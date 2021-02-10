import random
from collections import Counter
from multiprocessing import Pool

from game import Game, Player, RealState


def generate_players(balance):
    players = Player.from_strategies(balance)
    random.shuffle(players)
    return tuple(players)

def generate_properties(how_many, median=5, stdv=1, price_scale=20, rent_scale=10):
    distribution = (round(random.gauss(median, stdv)) for _ in range(how_many))
    params = ((value * price_scale, value * rent_scale) for value in distribution)
    return tuple(RealState(price, rent) for price, rent in params)

def game_factory():
    return Game(generate_players(300), generate_properties(20))


class Simulation:
    def __init__(self, population, pool=5):
        self.population = population
        self.pool = pool
        self.stats = {}

    def run(self):
        with Pool(self.pool) as p:
            winners = p.map(self.exercise, (n for n in range(self.population)))

        self.stats = Counter(winners)

    @staticmethod
    def exercise(_):
        game = game_factory()
        winner = game.run()
        return str(winner)

    def __str__(self):
        output = [f'Simulations: {self.population}']
        output += [f'- {k}: {v} {v / self.population * 100:.1f}%'
                   for k, v in sorted(self.stats.items(), key=lambda t: t[-1], reverse=True)]
        return '\n'.join(output)
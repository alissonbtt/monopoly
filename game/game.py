import random
from itertools import cycle

from game import Board


class Game:
    INITIAL_BALANCE = 300

    def __init__(self, players, properties):
        self.players = players
        self.board = Board(self.players, properties)

    @property
    def leader(self):
        return sorted(self.players,
                      key=lambda p: p.balance,
                      reverse=True)[0]

    @staticmethod
    def dice():
        return random.randint(1, 6)

    def run(self, counter=0):
        turn_count = counter

        for p in cycle(self.players):
            if p not in self.board.players:
                continue

            self.board.turn(p, self.dice())
            turn_count += 1

            if len(self.board.players) == 1:
                break

            if turn_count >= 1000:
                break

        return self.leader


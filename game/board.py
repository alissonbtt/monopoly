from game.player import AbortInvestment, NotEnoughMoney, OutOfMoney

BONUS = 100

class Board:
    def __init__(self, players, properties, bonus=BONUS):
        self.players = {p: -1 for p in players}
        self.properties = properties
        self.bonus = bonus

    def move(self, player, steps):
        cur_pos = self.players[player]
        new_lap, new_pos = divmod(cur_pos + steps, len(self))
        self.players[player] = new_pos

        if new_lap:
            player.receive(self.bonus)

        return self.properties[new_pos]

    def __len__(self):
        return len(self.properties)

    def remove(self, player):
        for rs in self.properties:
            if rs.owner_is(player):
                rs.foreclose()

        del self.players[player]

    def turn(self, player, steps):
        real_state = self.move(player, steps)

        try:
            real_state.deal(player)
        except (AbortInvestment, NotEnoughMoney):
            pass
        except OutOfMoney:
            self.remove(player)






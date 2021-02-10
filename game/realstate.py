class RealState:
    def __init__(self, price, rent, owner=None):
        self.price = price
        self.rent = rent
        self.owner = owner

    def has_owner(self):
        return self.owner is not None

    def owner_is(self, player):
        return self.owner is player

    def foreclose(self):
        self.owner = None

    def sell_to(self, player):
        assert not self.has_owner()

        player.invest(self.price, self.rent)
        self.owner = player

    def rent_to(self, player):
        if self.owner_is(player):
            return

        self.owner.receive(player.pay(self.rent))

    def deal(self, player):
        if self.has_owner():
            self.rent_to(player)
        else:
            self.sell_to(player)


class Players:

    def __init__(self, tally):
        self.tally = tally
        self.players = []

        for _ in range(tally):
            self.add_player()

    def add_player(self):
        name = input("Enter Player Name: ")
        self.players.append(str(name))

    def get_players(self):
        return self.players

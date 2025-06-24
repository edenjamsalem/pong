from ..game_logic.game import Game
from player import Player

class GameSession:
    def __init__(self, game: Game):
        self.game = game
        self.clients: list[Player] = []
        self.full: bool = False

    def add_client(self, player: Player):
        self.clients.append(player)

    def remove_client(self, player: Player):
        if player in self.clients:
            self.clients.remove(player)

from ..gameLogic.game import Game
from fastapi import WebSocket
from pydantic import BaseModel

class Input(BaseModel):
    type: str
    side: int
    dy: float

class Player(BaseModel):
    id: int
    side: int
    websocket: WebSocket
    input: Input

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

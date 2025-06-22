from ..gameLogic.game import Game
from fastapi import WebSocket

class GameSession:
    def __init__(self, game: Game):
        self.game = game
        self.clients: list[WebSocket] = []
        self.full: bool = False

    def add_client(self, websocket):
        self.clients.append(websocket)

    def remove_client(self, websocket):
        if websocket in self.clients:
            self.clients.remove(websocket)
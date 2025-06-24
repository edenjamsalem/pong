from ..settings import *
from fastapi import WebSocket
from ..game_logic.game import SinglePlayer, TwoPlayer, Tournament
import asyncio

class Client:
    def __init__(self, id, websocket):
        self.id: str = id
        self.websocket: WebSocket = websocket

class GameSession:
    def __init__(self,mode: str):
        self.mode = mode
        self.game = None
        self.clients: list[Client] = []
        self.full: bool = False
        self.running = False

    def add_client(self, client: Client):
        if not self.full:
            self.clients.append(client)
            if (self.mode == 'single_player' or self.mode == 'two_player_local') and len(self.clients) == 1:
                self.full = True
            elif self.mode == 'two_player_remote' and len(self.clients) == 2:
                self.full = True

    def remove_client(self, client: Client):
        if client in self.clients:
            self.clients.remove(client)
        if len(self.clients) == 0:
            self.running = False
            self.stop()

    async def _assign_sides(self): # need to think how this will work for the tournament
        if self.mode == 'two_player_remote':
            for i, client in enumerate(self.clients[:2]):
                client.side = i
                self.game.players[i].side = i
                await client.websocket.send_json({"side": i})
        elif self.mode == 'tournament':
            pass

    async def start(self):
        await self._assign_sides()
        if not self.running:
            self.running = True
            asyncio.create_task(self.game.run())
    
    def stop(self):
        self.running = False
        if self.game:
            self.game.running = False
    
    async def broadcast_callback(self, state):
        disconnected_clients = []
        for client in self.clients:
            try:
                await client.websocket.send_json(state)
            except:
                disconnected_clients.append(client)
        for client in disconnected_clients:
            self.remove_client(client)

def create_game_session(game_mode: str, game_id: str):
    game_session = GameSession(game_mode)

    if game_mode == 'single_player': 
        game = SinglePlayer(game_id, game_session.broadcast_callback)
    elif game_mode == "two_player_local" or game_mode == "two_player_remote":
        game = TwoPlayer(game_id, game_session.broadcast_callback)
    elif game_mode == "tournament":
        game = Tournament(game_id, game_session.broadcast_callback)
    else:
        raise ValueError(f"Invalid game mode '{game_mode}'")
    
    game_session.game = game
    return game_session

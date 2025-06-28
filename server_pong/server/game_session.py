from game_logic.game import SinglePlayer, TwoPlayer, Tournament
from .client import Client
import asyncio

class GameSession:
    def __init__(self, mode: str, game_id: str):
        self.mode = mode
        self.id = game_id
        self.clients: list[Client] = []
        self.full: bool = False
        self.running = False
        self._create_game()

    def _create_game(self):
        game_modes = {
            'single_player': SinglePlayer,
            'two_player_local': TwoPlayer,
            'two_player_remote': TwoPlayer,
            'tournament': Tournament
        }

        GameMode = game_modes.get(self.mode)
        if not GameMode:
            raise ValueError(f'Invalid game mode: {GameMode}')
            # maybe destroy here?
        
        self.game = GameMode(self.id, self.broadcast_callback)

    def add_client(self, client: Client):
        if not self.full:
            self.clients.append(client)
            if (self.mode == 'single_player' or self.mode == 'two_player_local') and len(self.clients) == 1:
                self.full = True
            elif self.mode == 'two_player_remote' and len(self.clients) == 2:
                self.full = True
            # need to add tournament 

    def remove_client(self, client: Client):
        if client in self.clients:
            self.clients.remove(client)
        if len(self.clients) == 0:
            self.stop()

    async def start(self):
        await self._assign_sides()
        if not self.running:
            self.running = True
            asyncio.create_task(self.game.run())
    
    def stop(self):
        self.running = False
        if self.game:
            self.game.running = False
    
    async def _assign_sides(self):
        # for single or two player local sides can be assigned client side ??
        if self.mode == 'two_player_remote':
            await self.clients[0].websocket.send_json({
                'type': 'side',
                'data': 'left'
            })
            await self.clients[1].websocket.send_json({
                'type': 'side',
                'data': 'right'
            })

        elif self.mode == 'tournament':  # need to think how this will work for the tournament
            pass
    
    async def broadcast_callback(self, state):
        for client in reversed(self.clients): # loop backward to avoid indexing issues when rm clients
            try:
                await client.websocket.send_json(state)
            except:
                self.remove_client(client)


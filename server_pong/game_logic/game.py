from .settings import * 
from .sprites import * 
from .utils import Clock
from abc import ABC, abstractmethod
from server.schemas.client_data import PaddleMovement
import asyncio

class Game(ABC):
    def __init__(self, id, broadcast_callback):
        self.id = id    # see if actually needed later
        self._broadcast = broadcast_callback
        self.clock = Clock()
        self.queue = asyncio.Queue()
        self.running = True

        # sprites 
        self._init_players()
        self.ball = Ball(self.players, self._update_score)

    # private methods
    def _update_score(self, side):
        self.players[side].score += 1

    @abstractmethod
    def _init_players(self):
        pass

    def _process_queue(self, dt):
        while not self.queue.empty():
            input = self.queue.get_nowait()
            self.players[input.side].move(dt, input.dy)
            self.queue.task_done()

    @abstractmethod
    def _handle_input(self, dt):
        pass

    def _update_state(self, dt):
        self.players["left"].cache_rect()
        self.players["right"].cache_rect()
        self.ball.cache_rect()
        self._handle_input(dt)
        self.ball.update(dt)

    # public methods
    def enqueue(self, input: PaddleMovement):
        self.queue.put(input)

    def get_state(self):
        return {
            'type' : 'state',
            'data' : {
                'player_left': {'y': self.players['left'].rect.y, 'score': self.players['left'].score,},
                'player_right': {'y': self.players['right'].rect.y, 'score': self.players['right'].score,},
                'ball': {'x': self.ball.rect.x, 'y': self.ball.rect.y},
            }
        }
    
    def _state_changed(self):
        return (
            self.players['left'].rect.y != self.players['left'].old_rect.y or
            self.players['right'].rect.y != self.players['right'].old_rect.y or
            self.ball.rect.x != self.ball.old_rect.x or
            self.ball.rect.y != self.ball.old_rect.y
        )

    async def run(self):
        while self.running:
            dt = await self.clock.tick(60) / 1000
            self._update_state(dt)
            if (self._state_changed()):
                state = self.get_state()
                await self._broadcast(state)

class SinglePlayer(Game):
    def _init_players(self):
        self.players = {"left": Player(POS['left']), 'right': AIBot(POS['right'])}

    def _handle_input(self, dt):
        self._process_queue(dt) # handles player movement
        self.players['right'].update(dt) # assuming the bot doesn't use the queue

# the current implementation should work for both local and remote players
class TwoPlayer(Game):
    def _init_players(self):
        self.players = {'left': Player(POS['left']), 'right': Player(POS['right'])}

    def _handle_input(self, dt):
        self._process_queue(dt)

class Tournament(Game):
    ...
    pass


# if __name__ == '__main__':
#     game = Game()
#     game.run()

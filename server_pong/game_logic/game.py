from server_pong.settings import * 
from sprites import * 
from utils import Clock
from abc import ABC, abstractmethod
from ..server.game_session import PaddleMovement
import asyncio

class Game(ABC):
    def __init__(self, id, broadcast_callback):
        self.id = id    # see if I actually need this later
        self._broadcast_callback = broadcast_callback
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
        self.players[LEFT_PADDLE].cache_rect()
        self.players[RIGHT_PADDLE].cache_rect()
        self._handle_input(dt)
        self.ball.update(dt)

    # public methods
    async def enqueue(self, input: PaddleMovement):
        await self.queue.put(input)

    def get_state(self):
        return {
            "paddle_left": {'y': self.players[0].rect.y, 'score': self.players[0].score,},
            "paddle_right": {'y': self.players[1].rect.y, 'score': self.players[1].score,},
            "ball": {'x': self.ball.rect.x, 'y': self.ball.rect.y},
        }

    async def run(self):
        while self.running:
            dt = await self.clock.tick(60) / 1000
            self._update_state(dt)
            state = self.get_state()
            await self._broadcast_callback(state)

class SinglePlayer(Game):
    def _init_players(self):
        self.players = (Player(side = LEFT_PADDLE), AIBot(side = RIGHT_PADDLE))

    def _handle_input(self, dt):
        self._process_queue(dt) # handles player movement
        self.players[RIGHT_PADDLE].update(dt) # assuming the bot doesn't use the queue

# the current implementation should work for both local and remote players
class TwoPlayer(Game):
    def _init_players(self):
        self.players = (Player(side = LEFT_PADDLE), Player(side = RIGHT_PADDLE))

    def _handle_input(self, dt):
        self._process_queue(dt)

class Tournament(Game):
    ...
    pass


# if __name__ == '__main__':
#     game = Game()
#     game.run()

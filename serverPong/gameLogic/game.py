from settings import * 
from sprites import * 
from utils import Clock
from queue import SimpleQueue
from abc import ABC, abstractmethod
from ..server.gameSession import Input

class Game(ABC):
    def __init__(self, id, broadcast_callback):
        self.id = id
        self.clock = Clock()
        self.queue = SimpleQueue()
        self.running = True
        # self.broadcast_state = broadcast_callback

        # sprites 
        self._init_players()
        self.ball = Ball((self.players[0], self.players[1]), self._update_score)

    # private methods
    def _update_score(self, side):
        self.players[side].score += 1

    @abstractmethod
    def _init_players(self):
        pass

    def _process_queue(self, dt):
        # need to add input validation
        while not self.queue.empty():
            input = self.queue.get_nowait()
            if input.type == 'movement':
                self.players[input.side].move(dt, input.dy)
            elif input.type == 'quit':
                # need to handle this properly
                print(f"Player '{input.side}' has quit the game!")
                self.running = False
                break
    
    @abstractmethod
    def _update_state(self, dt):
        pass

    # public methods
    def enqueue(self, input: Input):
        self.queue.put(input)

    def get_state(self):
        return {
            "player_left": {'y': self.players[0].rect.y, 'score': self.players[0].score,},
            "player_right": {'y': self.players[1].rect.y, 'score': self.players[1].score,},
            "ball": {'x': self.ball.rect.x, 'y': self.ball.rect.y},
        }

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self._update_state(dt)
            # self.broadcast_state(self.id, self.state)

class SinglePlayer(Game):
    def _init_players(self):
        self.players = (Player(side = LEFT_PADDLE), AIBot(side = RIGHT_PADDLE))
    
    def _update_state(self, dt):
        self.players[LEFT_PADDLE].cache_rect()
        self.players[RIGHT_PADDLE].cache_rect()
        self._process_queue(dt)
        self.players[RIGHT_PADDLE].update(dt) # assuming the bot doesn't use the queue
        self.ball.update(dt)

# the current implementation should work for both local and remote players
class TwoPlayer(Game):
    def _init_players(self):
        self.players = (Player(side = LEFT_PADDLE), Player(side = RIGHT_PADDLE))
    
    def _update_state(self, dt):
        self.players[LEFT_PADDLE].cache_rect()
        self.players[RIGHT_PADDLE].cache_rect()
        self._process_queue(dt)
        self.ball.update(dt)


class Tournament(Game):
    pass

# if __name__ == '__main__':
#     game = Game()
#     game.run()

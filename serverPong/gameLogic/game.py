from settings import * 
from sprites import * 
from utils import Clock
from queue import SimpleQueue

class Game:
    def __init__(self, id, mode, broadcast_callback):
        self.id = id
        self.clock = Clock()
        self.queue = SimpleQueue()
        self.running = True
        # self.broadcast_state = broadcast_callback

        # sprites 
        self.players = (Player(side = LEFT_PADDLE), Player(side = RIGHT_PADDLE))
        self.ball = Ball((self.players[0], self.players[1]), self._update_score)

    # private methods
    def _update_score(self, side):
        self.players[side].score += 1

    def _process_queue(self, dt):
        while not self.queue.empty():
            player_id, dy = self.queue.get_nowait()
            self.players[player_id].update(dt, dy)

    # public methods
    def queue_movement(self, side, dy):
        self.queue.put((side, dy))

    def get_state(self):
        return {
            "player1": {'y': self.players[0].rect.y, 'score': self.players[0].score,},
            "player2": {'y': self.players[1].rect.y, 'score': self.players[1].score,},
            "ball": {'x': self.ball.rect.x, 'y': self.ball.rect.y},
        }

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self._process_queue(dt)
            self.ball.update(dt)
            
            # self.broadcast_state(self.id, self.state)

# if __name__ == '__main__':
#     game = Game()
#     game.run()

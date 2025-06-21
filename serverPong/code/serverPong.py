from settings import * 
from sprites import * 
from utils import Clock
from queue import SimpleQueue
import json

class Game:
    def __init__(self, id, broadcast_callback):
        self.id = id
        self.clock = Clock()
        self.running = True
        self.queue = SimpleQueue()
        self.broadcast_state = broadcast_callback

        # sprites 
        self.player1 = Player('player1')
        self.player2 = Player('player2')
        self.ball = Ball((self.player1, self.player2), self._update_score)

        # game state
        self.state = {
            "player1": {'y': self.player1.rect.y, 'dy': 0},
            "player2": {'y': self.player2.rect.y, 'dy': 0},
            "ball": {'x': self.ball.rect.x, 'y': self.ball.rect.y},
            "score": {'player1': 0, 'player2': 0}
        }

    def _update_score(self, player):
        self.state['score'][player] += 1

    def _update_state(self):
        self.state['player1']['y'] = self.player1.rect.y
        self.state['player2']['y'] = self.player2.rect.y
        self.state['ball']['x'] = self.ball.rect.x
        self.state['ball']['y'] = self.ball.rect.y
        # need to send a 'dy = 0' API request on player's keyup !

    def _process_queue(self):
        while not self.queue.empty():
            player, movement = self.queue.get_nowait()
            self.state[player]['dy'] = movement

    # called externally by server only upon API post request
    def queue_movement(self, player, dy):
        self.queue.put((player, dy))

    def get_state(self):
        return (self.state.copy())

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self._process_queue()
            
            # update
            self.player1.update(dt, self.state['player1']['dy'])
            self.player2.update(dt, self.state['player2']['dy'])
            self.ball.update(dt)
            self._update_state()
            
            self.broadcast_state(self.id, self.state)

if __name__ == '__main__':
    game = Game()
    game.run()
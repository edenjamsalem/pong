from settings import * 
from sprites import * 
from utils import Clock
from queue import SimpleQueue
import json

class Game:
    def __init__(self, id):
        self.id = id
        self.clock = Clock()
        self.running = True
        self.queue = SimpleQueue()

        # sprites 
        self.player1 = Player('player1')
        self.player2 = Player('player2')
        self.ball = Ball((self.player1, self.player2), self.update_score)

        # score 
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0, 'opponent': 0}

        # game state
        self.state = {
            "player1": {'y': self.player1.rect.y, 'dy': 0},
            "player2": {'y': self.player2.rect.y, 'dy': 0},
            "ball": {'x': self.ball.rect.x, 'y': self.ball.rect.y},
            "score": {'player': 0, 'player2': 0}
        }


    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def update_state(self):
        self.state['player1']['y'] = self.player1.rect.y
        self.state['player2']['y'] = self.player2.rect.y
        self.state['ball']['x'] = self.ball.rect.x
        self.state['ball']['y'] = self.ball.rect.y
        # need to send a dy = 0 on player's keyup !

    def broadcast_state(self):
        pass

    # called externally by server only upon API post request
    def queue_movement(self, player, dy):
        self.queue.put((player, dy))

    def process_queue(self):
        while not self.queue.empty():
            player, movement = self.queue.get_nowait()
            self.state[player]['dy'] += movement

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.process_queue()
            
            # update
            self.player1.update(dt, self.state['player1']['dy'])
            self.player2.update(dt, self.state['player2']['dy'])
            self.ball.update(dt)
            self.update_state()
            
            self.broadcast_state()

if __name__ == '__main__':
    game = Game()
    game.run()
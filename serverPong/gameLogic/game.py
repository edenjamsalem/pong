from settings import * 
from sprites import * 
from utils import Clock
from queue import SimpleQueue

class Game:
    def __init__(self, id, mode, broadcast_callback):
        self.id = id
        self.clock = Clock()
        self.running = True
        self.queue = SimpleQueue()
        self.broadcast_state = broadcast_callback

        # sprites 
        self.player1 = Player('player1')
        if mode == 'two_player':
            self.player2 = Player('player2')
        # elif mode == 'single_player':
        #     self.player2 = AIBot()
        self.ball = Ball((self.player1, self.player2), self._update_score)

        self.score = {'player1': 0, 'player2': 0}

    # private methods
    def _update_score(self, player):
        pass

    def _process_queue(self):
        while not self.queue.empty():
            player, movement = self.queue.get_nowait()

    # public methods
    def queue_movement(self, player, dy):
        self.queue.put((player, dy))

    def get_state(self):
        return ()

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
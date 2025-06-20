from settings import * 
from sprites import * 
from utils import Clock, Group
import json

class Game:
    def __init__(self):
        self.clock = Clock()
        self.running = True

        # sprites 
        self.player1 = Player('player1')
        self.player2 = Player('player2')
        self.ball = Ball((self.player1, self.player2), self.update_score)
                    
        # groups
        self.all_sprites = Group(self.display_surface)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.ball)

        # score 
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0, 'opponent': 0}

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.running = False
            #         with open(join('data', 'score.txt'), 'w') as score_file:
            #             json.dump(self.score, score_file)
            
            # update 
            self.all_sprites.update(dt)

if __name__ == '__main__':
    game = Game()
    game.run()
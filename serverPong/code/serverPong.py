from settings import * 
from sprites import * 
from utils import Clock, Group
import json

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
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
        self.font = pygame.font.Font(None, 160)

    def display_score(self):
        # player 
        player_surf = self.font.render(str(self.score['player']), True, COLOURS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLOURS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        # line separator
        pygame.draw.line(self.display_surface, COLOURS['bg detail'], (WINDOW_WIDTH /2, 0), (WINDOW_WIDTH /2, WINDOW_HEIGHT), 6)

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(join('data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)
            
            # update 
            self.all_sprites.update(dt)
            # self.player1.update(dt)
            # self.player2.update(dt)
            # self.ball.update(dt)

            # draw 
            self.display_surface.fill(COLOURS['bg'])
            self.display_score()
            self.all_sprites.draw()
            # self.display_surface.blit(self.player1.image, (self.player1.rect.x, self.player1.rect.y))
            # self.display_surface.blit(self.player2.image, (self.player2.rect.x, self.player2.rect.y))
            # self.display_surface.blit(self.ball.image, (self.ball.rect.x, self.ball.rect.y))
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
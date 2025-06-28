from .settings import * 
from .utils import Rect
from random import choice, uniform
import time
import numpy as np
from abc import ABC

class Paddle(ABC):
    def __init__(self):
        self.rect = Rect(POS["left"][0], POS["left"][1], SIZE['paddle'][0], SIZE['paddle'][1])
        self.old_rect = self.rect.instance()
    
    def move(self, dt, dy):
        self.rect.y += dy * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom   

    def cache_rect(self):
        self.old_rect.copy(self.rect)

class Player(Paddle):
    def __init__(self, pos):
        super().__init__()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = SPEED['player']
        self.score = 0

class AIBot(Paddle):
    def __init__(self, pos):
        super().__init__()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        ... 
    
    def update(self, dt):
        ...
        pass

class Ball():
    def __init__(self, players, update_score):
        self.players: dict[str, Paddle] = players
        self.update_score = update_score

        # rect & movement
        self.rect = Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, SIZE['ball'][0], SIZE['ball'][1])
        self.old_rect = self.rect.instance()
        self.direction = np.array([choice((1,-1)), uniform(0.7, 0.8) * choice((-1,1))])
        self.speed_modifier = 0
    
        # timer 
        self.start_time = time.time()

    def move(self, dt):
        self.rect.x += self.direction[0] * SPEED['ball'] * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.y += self.direction[1] * SPEED['ball'] * dt * self.speed_modifier
        self.collision('vertical')
    
    def collision(self, direction):
        for paddle in self.players.values():
            if self.rect.colliderect(paddle.rect):
                if direction == 'horizontal':
                    if self.rect.right >= paddle.rect.left and self.old_rect.right <= paddle.old_rect.left:
                        self.rect.right = paddle.rect.left
                        self.direction[0] *= -1
                    elif self.rect.left <= paddle.rect.right and self.old_rect.left >= paddle.old_rect.right:
                        self.rect.left = paddle.rect.right
                        self.direction[0] *= -1
                else:
                    if self.rect.bottom >= paddle.rect.top and self.old_rect.bottom <= paddle.old_rect.top:
                        self.rect.bottom = paddle.rect.top
                        self.direction[1] *= -1
                    elif self.rect.top <= paddle.rect.bottom and self.old_rect.top >= paddle.old_rect.bottom:
                        self.rect.top = paddle.rect.bottom
                        self.direction[1] *= -1

    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction[1] *= -1
        
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction[1] *= -1
        
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score("right" if self.rect.x < WINDOW_WIDTH / 2 else "left")
            self.reset()
        
    def reset(self):
        self.rect.x = WINDOW_WIDTH / 2
        self.rect.y = WINDOW_HEIGHT / 2
        self.direction = np.array([choice((1,-1)), uniform(0.7, 0.8) * choice((-1,1))])
        self.start_time = time.time()
    
    # def cache_rect(self):
    #     self.old_rect.copy(self.rect)

    def delay_timer(self):
        if (time.time()) - self.start_time >= START_DELAY:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect.copy(self.rect)
        self.delay_timer()
        self.move(dt)
        self.wall_collision()
from settings import *
import time

class Clock:
    def __init__(self):
        self.last_time = time.time()

    def tick(self, fps=0):
        current_time = time.time()
        delta = current_time - self.last_time
        self.last_time = current_time

		# account for sleep time
        if fps > 0:
            sleep_time = max(0, (1.0 / fps) - delta)
            time.sleep(sleep_time)
            delta += sleep_time

        return delta * 1000

class Rect:
	def __init__(self, x: float, y: float, w: float, h: float):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	@property
	def left(self):
		return self.x
		
	@left.setter
	def left(self, value):
		self.x = value
	
	@property
	def right(self):
		return self.x + self.w
	
	@right.setter
	def right(self, value):
		self.x = value - self.w
	
	@property
	def top(self):
		return self.y
	
	@top.setter
	def top(self, value):
		self.y = value
	
	@property
	def bottom(self):
		return self.y + self.h
	
	@bottom.setter
	def bottom(self, value):
		self.y = value - self.h
		
	def colliderect(self, other):
		return (
			self.left < other.right and
			self.right > other.left and 
			self.top < other.bottom and
			self.bottom > other.top
		)
	
	def copy(self, other):
		self.x = other.x
		self.y = other.y
		self.w = other.w
		self.h = other.h

	def instance(self):
		return Rect(self.x, self.y, self.w, self.h)

class Group:
	def __init__(self, display_surface):
		self.sprites = []
		self.display_surface = display_surface

	def add(self, sprite):
		self.sprites.append(sprite)

	def update(self, dt):
		for sprite in self.sprites:
			sprite.update(dt)

	def draw(self):
		for sprite in self.sprites:
			self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

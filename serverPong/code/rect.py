from settings import *


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

from serverPong.utils import Clock
from queue import SimpleQueue

class Client():
	def __init__(self, id):
		self.id = id
		self.clock = Clock()
		self.queue = SimpleQueue()
		self.running = True
		...

	def run(self):
		while self.running:
			# handle any queue'd server state updates
			# render the graphic
			# get user input & send API put requests to server
			pass
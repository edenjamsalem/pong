from ..game_logic.utils import Clock
import asyncio
import websockets
import json

# ball collisions wills be handled by the server, but wall collisions with the paddle
# should be checked and ignored when input is received to prevent us flooding the 
# server with unnecessary PaddleMovement requests

class Client():
	def __init__(self, id):
		self.uri = "ws://localhost:8000/ws/single_player"
		self.id = id
		self.clock = Clock()
		self.queue = asyncio.Queue()
		self.running = True
		...

# asyncio.run(listen())
	async def run(self):
		async with websockets.connect(self.uri) as websocket:
			while self.running:
				# handle any queued server state updates
				msg = await websocket.recv()
				data = json.loads(msg)
				print("Received:", data)

				# render the graphic
				...

				# get user input & send API put requests to server
				...

if __name__ == '__main__':
	client = Client()
	client.run()
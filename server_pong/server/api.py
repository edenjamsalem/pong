from server_pong.settings import *
from fastapi import FastAPI, HTTPException, WebSocket
from uuid import uuid4
from threading import Thread
from ..game_logic.game import Game
from game_session import GameSession, Player
import asyncio

api = FastAPI()
game_sessions = {}

# Websocket endpoints
@api.websocket("ws")
async def websocket_endpoint(ws: WebSocket, game_id: str):
    await ws.accept()
    game = Game(game_id)
    player = Player(id=0, side=LEFT_PADDLE, websocket=ws)
    game.add_player(player)

    try:
        while (True):
            data = await ws.receive_json()
            game.enqueue(data)

    except:

    

# HTTP endpoints (NOT FAST ENOUGH FOR USER INPUT)
@api.post("/games")
def create_game():
    game_id = str(uuid4())
    game = Game(game_id)
    game_sessions[game_id] = GameSession(game)

    thread = Thread(target=game.run, daemon=True)
    thread.start()
    return {"game_id": game_id}

@api.get("/games/{game_id}/state")
def get_game_state(game_id: str):
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Item not found")
    return game_sessions[game_id].get_state()

@api.put("/games/{game_id}/input")
def put_user_input(game_id: str, player: Player):
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Item not found")
    game_sessions[game_id].enqueue(player.input)
    return {"status": "input queued"}


# Handles creating new games and joining a game
	# POST /games           → Create a new game
	# POST /games/{id}/join → Join a game by ID
	# GET  /games           → List active games

# Handles user input updates & user game state requests
	# POST /games/{id}/input     → Send input for paddle movement
	# GET  /games/{id}/state     → Get current state for rendering

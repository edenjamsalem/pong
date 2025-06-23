from fastapi import FastAPI, HTTPException
from uuid import uuid4
from threading import Thread
from ..gameLogic.game import Game
from gameSession import GameSession, Player

app = FastAPI()
game_sessions = {}

# @app.websocket("ws")
# async def websocket_endpoint(ws: WebSocket):
#     await ws.accept()

#     while True:
#         data = ws.receive_json()

# Endpoints
# need to do proper input validation for API endpoints !

@app.post("/games")
def create_game():
    game_id = str(uuid4())
    game = Game(game_id)
    game_sessions[game_id] = GameSession(game)

    thread = Thread(target=game.run, daemon=True)
    thread.start()
    return {"game_id": game_id}

@app.get("/games/{game_id}/state")
def get_game_state(game_id: str):
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Item not found")
    return game_sessions[game_id].get_state()

@app.put("/games/{game_id}/input")
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

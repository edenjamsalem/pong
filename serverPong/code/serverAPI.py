from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from threading import Thread
from serverPong import Game

class PlayerInput(BaseModel):
    player: str
    dy: int

app = FastAPI()

# Store all active games
games: dict[str, Game] = {}

@app.post("/games")
def create_game():
    game_id = str(uuid4())
    game = Game(game_id)
    games[game_id] = game

    thread = Thread(target=game.run, daemon=True)
    thread.start()
    return {"game_id": game_id}

@app.get("/games/{game_id}/state")
def get_game_state(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Item not found")
    return games[game_id].get_state()

@app.put("/games/{game_id}/input")
def put_user_input(game_id:str, input: PlayerInput):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Item not found")
    games[game_id].queue_movement(input.player, input.dy)
    return {"status": "input queued"}

# Handles creating new games and joining a game
	# POST /games           → Create a new game
	# POST /games/{id}/join → Join a game by ID
	# GET  /games           → List active games

# Handles user input updates & user game state requests
	# POST /games/{id}/input     → Send input for paddle movement
	# GET  /games/{id}/state     → Get current state for rendering

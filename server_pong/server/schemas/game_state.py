from pydantic import BaseModel
from typing import Literal

# submodels
class Ball(BaseModel):
	'x' : float
	'y' : float

class Player(BaseModel):
	'y' : float
	'score' : int

class GameState(BaseModel):
	player_left : Player
	player_right : Player
	ball : Ball


# top-level model

class GameStateMessage(BaseModel):
	type : Literal['state']
	data : GameState
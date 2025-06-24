from pydantic import BaseModel, Literal, Union
from fastapi import WebSocket

class MovementInput(BaseModel):
    type: Literal['movement']
    side: int
    dy: float

class QuitInput(BaseModel):
    type: Literal['quit']
    side: int

class InitInput(BaseModel):
    type: Literal['init']
    mode: str

Input = Union[MovementInput, QuitInput]

class Player(BaseModel):
    id: int
    side: int
    websocket: WebSocket
    input: Input = None
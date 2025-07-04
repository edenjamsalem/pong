from pydantic import BaseModel, TypeAdapter
from typing import Literal, Union

class PaddleMovement(BaseModel):
    client_id: str
    type: Literal['movement']
    side: Literal['left', 'right']
    dy: float

class QuitGame(BaseModel):
    client_id: str
    type: Literal['quit']

client_data = Union[PaddleMovement, QuitGame]
data_adaptor = TypeAdapter(client_data)

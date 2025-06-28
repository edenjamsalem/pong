from pydantic import BaseModel
from typing import Literal

class Message(BaseModel):
	client_id: str
	type: Literal['error']
	data: str


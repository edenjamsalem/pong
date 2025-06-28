from fastapi import WebSocket
from pydantic import BaseModel

# class Client:
#     def __init__(self, id, username, password):
#         self.id: str = id
#         self.username: str = username
#         self.password: str = password
#         self.websocket: WebSocket = None

class Client(BaseModel):
    id: str
    username: str = 'guest'
    password: str
    websocket: WebSocket = None
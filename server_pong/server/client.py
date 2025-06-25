from fastapi import WebSocket

class Client:
    def __init__(self, id, username, password):
        self.id: str = id
        self.username: str = username
        self.password: str = password
        self.websocket: WebSocket = None

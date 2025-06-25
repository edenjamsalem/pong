'''
    -   This page creates the API and its endpoints using FastAPI

    -   FastAPI is designed to work with python's "async" feature rather than using threads

    -   HTTP requests are slow and are only used to make the inititial request to 
        create a new game and to reigister a client

    -   After that, a websocket is established for real-time connection with the client

    -   One websocket is used for a single client and handles all subsequent API requests

    -   A client is a single device not a single player, there can be two players on a single
        keyboard, sending requests via the same websocket to the same game session
'''

# TODO: need to create a standardised JSON structure that we stick to for client-server communication

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uuid import uuid4
from game_session import GameSession
from client import Client
from msg_data import data_adaptor
from pydantic import ValidationError

api = FastAPI()
game_sessions = {}
clients = {}    # only temporay, we will use a db to store this

# Websocket endpoints

# creates a new websocket, adds it to the client and adds the client to the game session
# specified by the game_id, if the game is now full it will start automatically
@api.websocket("/ws/{game_mode}/{game_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str, game_id: str):  
    # initial connection

    if client_id not in clients:
        await ws.close(code=4004, reason="Client not recognised.")
        return
    if game_id not in game_sessions:
        await ws.close(code=4004, reason="Game not found.")
        return
    
    await ws.accept()
    game_session = game_sessions[game_id]
    if game_session.full:
        await ws.close(code=4004, reason="Game already full.")
        return

    client = clients[client_id]
    client.websocket = ws
    game_session.add_client(client)

    if not game_session.full:
        await ws.send_json({"message": "Waiting for more players"})
    elif not game_session.running:
        await game_session.start()
    
    # gameplay requests
    try:
        while (True):
            json_data = await ws.receive_json()
            try:
                # converts json to pydantic BaseModel for automatic type checking
                client_data = data_adaptor.validate_python(json_data) 
            except ValidationError as e:
                await ws.send_json({"error": "Invalid data format", "detail": e.errors()})
                continue 

            if client_data.type == 'movement':
                game_session.game.enqueue(client_data)
            elif client_data.type == 'quit':
                # handle quit properly
                pass

    except WebSocketDisconnect:
        game_session.remove_client(client)
        # need to handle this more thoroughly


# HTTP endpoints

# creates a new game_session and return game_id
@api.post("/games/{game_mode}")
def create_game(client_id: str, game_mode: str):
    if client_id not in clients:
        # placeholder for real return value
        return {"error": "cleint_id not found"}
    
    id = str(uuid4())
    game_sessions[id] = GameSession(game_mode, id)
    return {"game_id": id}
    

# creates a new client and returns their id
@api.post("/games/client")
def create_client(username, password):
    id = str(uuid4())
    # need to perform some sort of check with a db here
    clients[id] = Client(id, username, password)
    return {'client_id': id}


'''
    -   This page contains the API and its endpoints using FastAPI

    -   FastAPI is designed to work with python's "async" feature rather than using threads:
            https://docs.python.org/3/library/asyncio.html

    -   HTTP requests are slow and are only used to make the inititial request to 
        create a new game and to reigister a client

    -   After that, a websocket is established for real-time connection with the client

    -   One websocket is used for a single client and handles all subsequent API requests

    -   A client is a single device not a single player, there can be two players on a single
        keyboard, sending requests via the same websocket to the same game session

    -   To run the server from the route directory: "uvicorn server.api:api --reload".
        (depending on your terminal and python version you may need to prefix with "python3 -m" or "python -m")

    -   This starts the uvicorn server and tells it to execute the api object from the "server.api" file 
'''

# TODO: need to create a standardised JSON structure that we stick to for client-server communication
# TODO: If the API keeps growing maybe refactor into a class to share data more easily

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uuid import uuid4
from .game_session import GameSession
from .client import Client
from .schemas.client_data import data_adaptor
from pydantic import ValidationError

api = FastAPI()
game_sessions = {}
clients = {}    # only temporay, we will use a db to store this

# Websocket endpoints

async def validate_connection(ws: WebSocket, client_id: str, game_id: str):
    if client_id not in clients:
        await ws.close(code=4004, reason='Client not recognised.')
        return None, None
    if game_id not in game_sessions:
        await ws.close(code=4004, reason='Game not found.')
        return None, None
    
    return clients[client_id], game_sessions[game_id]

async def join_game_session(ws, client, game_session):
    if game_session.full:
        await ws.close(code=4004, reason='Game already full.')
        return 

    client.websocket = ws
    game_session.add_client(client)

    if not game_session.full:
        await ws.send_json({
            'type': 'message', 
            'data' : 'Waiting for more players'
        })
    elif not game_session.running:
        await game_session.start()

async def handle_client_messages(ws, game_session):
    while (True):
        json_data = await ws.receive_json()
        try:
            # converts json to pydantic BaseModel for automatic type checking
            client_data = data_adaptor.validate_python(json_data) 
        except ValidationError:
            await ws.send_json({
                'type': 'error',
                'data': 'Invalid data format'
            })
            continue 

        if client_data.type == 'movement':
            game_session.game.enqueue(client_data)
        elif client_data.type == 'quit':
            # handle quit properly
            pass

@api.websocket("/ws/{game_id}/{client_id}")
async def websocket_endpoint(ws: WebSocket, game_id: str, client_id: str):  

    # initial connection
    client, game_session = await validate_connection(ws, client_id, game_id)
    if not client or not game_session:
        return
    
    await ws.accept()
    await join_game_session(ws, client, game_session)

    # gameplay requests
    try:
        await handle_client_messages(ws, game_session)
    except WebSocketDisconnect:
        game_session.remove_client(client)
        # need to handle this more thoroughly


# HTTP endpoints

# creates a new game_session and return game_id
@api.post("/games/{game_mode}")
async def create_game(client_id: str, game_mode: str):
    if client_id not in clients:
        return {
            'type': 'error',
            'data': 'client id not found'
        }
    
    game_id = str(uuid4())
    try:
        game_sessions[game_id] = GameSession(game_mode, game_id)
        return {
            'type': 'game_created',
            'data': {'game_id': game_id}
        }
    except ValueError:
        return {
            'type': 'error',
            'data': f'Invalid game mode: {game_mode}'
        }
    

# creates a new client and returns their id
@api.post("/games/client")
async def create_client(username: str, password: str):
    # need to perform some sort of check with a db here
    client_id = str(uuid4())
    clients[client_id] = Client(client_id, username, password)
    return {
        'type': 'client_registered',
        'data': {'client_id': client_id}
    }

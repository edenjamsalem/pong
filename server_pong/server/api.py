'''
    -   This page creates the API and its endpoints using FastAPI

    -   FastAPI is designed to work with python's "async" feature rather than using threads

    -   HTTP requests are slow and are only used to make the inititial request to 
        create a new game

    -   After that, a websocket is established for real-time connection with the client

    -   One websocket is used for a single client and handles all subsequent API requests

    -   A client is a single device not a single player, there can be two players on a single
        keyboard, sending requests via the same websocket to the same game session
'''

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uuid import uuid4
from game_session import GameSession, Client
from server_pong.server.data import data_adaptor

api = FastAPI()
game_sessions = {}

# Websocket endpoints

@api.websocket("/ws/{game_mode}/{game_id}")
async def websocket_endpoint(ws: WebSocket, game_id: str):  
    # initial connection
    if game_id not in game_sessions:
        await ws.close(code=4004, reason="Game not found.")
        return
    
    await ws.accept()
    game_session = game_sessions[game_id]
    if game_session.full:
        await ws.close(code=4004, reason="Game already full.")
        return

    client = Client(id=str(uuid4()), websocket=ws)
    await ws.send_json({"client_id": client.id})
    game_session.add_client(client)

    if game_session.full and not game_session.running:
        await game_session.start()
    
    # gameplay requests
    try:
        while (True):
            json_data = await ws.receive_json()
            client_data = data_adaptor.validate_python(json_data) # converts the json to a pydantic BaseModel and performs type checking
            if client_data.type == 'movement':
                await game_session.game.enqueue(client_data)
            elif client_data.type == 'quit':
                # handle quit properly
                pass

    except WebSocketDisconnect:
        game_session.remove_client(client)
        # need to handle this more thoroughly

# HTTP endpoints (not fast enough to handle real-time communication)
@api.post("/games/{game_mode}")
def create_game(game_mode: str):
    game_id = str(uuid4())
    game_session = GameSession(game_mode, game_id)
    game_sessions[game_id] = game_session
    return {"game_id": game_id}

# @api.get("/games/{game_id}/state")
# def get_game_state(game_id: str):
#     if game_id not in game_sessions:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return game_sessions[game_id].get_state()

# @api.put("/games/{game_id}/input")
# def put_user_input(game_id: str, player: Player):
#     if game_id not in game_sessions:
#         raise HTTPException(status_code=404, detail="Item not found")
#     game_sessions[game_id].enqueue(player.input)
#     return {"status": "input queued"}


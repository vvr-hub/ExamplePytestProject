# utils/websocket_utils.py


async def send_message(websocket, message):
    await websocket.send(message)


async def receive_message(websocket):
    return await websocket.recv()


async def ping_pong(websocket):
    await websocket.ping()
    await websocket.pong()

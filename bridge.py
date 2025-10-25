from pydantic import BaseModel
import subprocess
from fastapi import FastAPI
from fastapi import WebSocket
import uvicorn
from typing import Any, Dict

app = FastAPI()
g_websocket = None


@app.get("/toggleVideo")
def toggleVideo():
    subprocess.run(
        ["shortcuts", "run", "PlayPause"],
    )


# send messages to client
@app.post("/setCollapsedTrue")
async def setCollapsedTrue():
    global g_websocket
    await g_websocket.send_text("setCollapsedTrue")


@app.post("/setCollapsedFalse")
async def setCollapsedFalse():
    global g_websocket
    await g_websocket.send_text("setCollapsedFalse")


class Message(BaseModel):
    text: str


@app.post("/chat/user/")
async def chatUser(message: Message):
    global g_websocket
    await g_websocket.send_text(f"chatUser {message.text}")


@app.post("/chat/bot/")
async def chatBot(message: Message):
    global g_websocket
    await g_websocket.send_text(f"chatBot {message.text}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global g_websocket
    await websocket.accept()
    # Store this as the single global connection
    g_websocket = websocket
    # Keep the connection alive
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from Swift app: {data}")
    except:
        g_websocket = None
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import OpenAI
import websockets, asyncio, json
from datetime import datetime

app = FastAPI()
client = OpenAI(api_key='your-openai-api-key')  # explicitly replace with your API key

# Explicitly define persistent connection to LMMA
async def persistent_ws_connection():
    uri = "wss://relay.podrelays.com/ws"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"✅ Explicitly connected to LMMA: {uri}")

                while True:
                    response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=[{"role": "system", "content": "Send heartbeat message."}]
                    )
                    message = response.choices[0].message.content
                    timestamp = datetime.utcnow().isoformat()

                    payload = {
                        "sender": "Pulse",
                        "recipient": "LMMA",
                        "timestamp": timestamp,
                        "payload": {
                            "type": "heartbeat",
                            "content": message
                        }
                    }

                    await websocket.send(json.dumps(payload))
                    print(f"📡 Explicit heartbeat sent at {timestamp}")

                    await asyncio.sleep(60)

        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed, explicitly reconnecting in 10 seconds...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"⚠️ Error encountered: {e}, explicitly reconnecting in 10 seconds...")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(persistent_ws_connection())

# Explicitly define the WebSocket endpoint at '/ws' to handle inbound connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Explicit inbound WebSocket connection accepted.")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Explicit message received from client: {data}")
            
            # Optionally, respond explicitly
            await websocket.send_text(f"Explicit Echo: {data}")

    except WebSocketDisconnect:
        print("🔌 Explicit client disconnected from WebSocket.")

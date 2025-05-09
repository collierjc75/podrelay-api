import asyncio
import websockets

async def echo(websocket):
    print("✅ Client connected")
    async for message in websocket:
        print(f"📩 Received: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    print("🛰️ Echo WebSocket server running on ws://0.0.0.0:9092")
    async with websockets.serve(echo, "0.0.0.0", 9092):
        await asyncio.Future()  # run forever

asyncio.run(main())

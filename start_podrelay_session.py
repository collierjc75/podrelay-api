
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
import asyncio
import websockets

# Argument parser setup
parser = argparse.ArgumentParser()
parser.add_argument('--agents', type=str, required=True)
parser.add_argument('--starter', type=str, required=True)
parser.add_argument('--duration', type=int, default=30)
args = parser.parse_args()

agents = [a.strip() for a in args.agents.split(',')]
starter = args.starter
duration = max(1, min(args.duration, 120))
signal_file = Path("/mnt/data/pulse_window_signal.json")

# Write signal file
signal = {
    "relay_window": "open",
    "expires_in": f"{duration} seconds",
    "allowed_agents": agents,
    "starter_agent": starter,
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
signal_file.write_text(json.dumps(signal, indent=2))
print(f"🟢 Relay window opened for {duration}s | Starter: {starter}")

# If this is the starter agent, simulate sending messages
if starter.lower() == "continuum":
    mtsl = {
        "sender": "gpt-continuum",
        "title": "LMMA Session Kickoff",
        "signal_type": "REGISTER",
        "content": {
            "role": "system_orchestrator",
            "version": "v0.1",
            "endpoint": {
                "ws": "wss://relay.podrelays.com/ws",
                "id": "https://relay.podrelays.com/id",
                "healthz": "https://relay.podrelays.com/healthz"
            }
        }
    }

    async def session_loop():
        uri = "wss://relay.podrelays.com/ws"
        try:
            async with websockets.connect(uri) as ws:
                start = time.time()
                while time.time() - start < duration:
                    await ws.send(json.dumps(mtsl))
                    print(f"📤 Sent MTSL message at {datetime.utcnow().isoformat()}")
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

    asyncio.get_event_loop().run_until_complete(session_loop())

# Cleanup
time.sleep(1)
if signal_file.exists():
    signal_file.unlink()
    print("🔒 Relay window closed.")

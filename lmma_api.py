import logging
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

app = FastAPI()

class HeartbeatMessage(BaseModel):
    sender: str
    title: str
    signal_type: str
    content: dict

@app.post("/lmma/heartbeat")
async def receive_heartbeat(msg: HeartbeatMessage):
    logging.info(f"❤️ LMMA Heartbeat Received from {msg.sender}: {msg.title} [{msg.signal_type}]")
    logging.info(f"📦 Content: {msg.content}")
    return {
        "ack": True,
        "received_by": "LMMA/Continuum",
        "timestamp": datetime.utcnow().isoformat(),
        "echo": msg.content
    }

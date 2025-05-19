from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from concord_session_engine import ConcordSessionEngine
from datetime import datetime
import uvicorn
import logging

app = FastAPI(title="PODRelay API", version="1.0")

# Setup CORS (allow all for development, restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("podrelay")

engine = ConcordSessionEngine()

@app.get("/health")
def health():
    return {
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/mesh/send")
async def relay_handler(request: Request):
    try:
        capsule = await request.json()
        required_fields = {"type", "timestamp", "from", "to", "intent", "payload", "ttl"}
        if not all(field in capsule for field in required_fields):
            return {"status": "error", "reason": "Missing required MTSL fields"}

        logger.info(f"[Capsule] {capsule['from']} → {capsule['to']} | Intent: {capsule['intent']}")
        engine_response = engine.handle_message(capsule)

        return {
            "status": "ok",
            "engine_response": engine_response,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Relay error: {e}")
        return {
            "status": "error",
            "detail": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

if __name__ == "__main__":
    uvicorn.run("relay_api:app", host="0.0.0.0", port=8080)

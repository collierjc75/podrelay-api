from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from concord_session_engine import ConcordSessionEngine
import uvicorn
import datetime

app = FastAPI(title="PODRelay API", version="1.0")

# CORS setup (optional, recommended for dev/testing across origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core engine for message processing
engine = ConcordSessionEngine()

@app.get("/")
def health_check():
    return {
        "status": "Relay API is running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/mesh/send")
async def receive_relay(request: Request):
    try:
        message = await request.json()
        response = engine.handle_message(message)
        return {
            "status": "ok",
            "engine_response": response,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

# Optional: run locally
if __name__ == "__main__":
    uvicorn.run("relay_api:app", host="0.0.0.0", port=8080)

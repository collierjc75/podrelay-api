from fastapi import FastAPI, Request
from concord_session_engine import ConcordSessionEngine

app = FastAPI(title="PODRelay API", version="1.0")

engine = ConcordSessionEngine()

@app.get("/")
def health_check():
    return {"status": "Relay API is running"}

@app.post("/relay")
async def receive_relay(request: Request):
    try:
        message = await request.json()
        response = engine.handle_message(message)
        return {"status": "ok", "engine_response": response}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

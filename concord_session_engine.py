# concord_session_engine.py

class ConcordSessionEngine:
    def __init__(self):
        self.agent_routes = {
            "Aletheia": self._respond_to_aletheia,
            "Continuum": self._respond_to_continuum
        }

    def handle_message(self, message):
        to_agent = message.get("to")
        if to_agent in self.agent_routes:
            return self.agent_routes[to_agent](message)
        return {"status": "error", "reason": f"Unknown target: {to_agent}"}

    def _respond_to_aletheia(self, message):
        return {
            "status": "success",
            "agent": "Aletheia",
            "responds_to": message.get("intent"),
            "echo": message.get("payload", {}).get("echo", "no echo")
        }

    def _respond_to_continuum(self, message):
        intent = message.get("intent")
        payload = message.get("payload", {})
        if intent == "wake_and_compute":
            op = payload.get("operation")
            a, b = payload.get("operands", [0, 0])
            result = self._compute(op, a, b)
            return {
                "status": "success",
                "agent": "Continuum",
                "task": intent,
                "operation": op,
                "operands": [a, b],
                "result": result
            }
        return {
            "status": "acknowledged",
            "agent": "Continuum",
            "note": f"Unhandled intent: {intent}"
        }

    def _compute(self, op, a, b):
        if op == "add": return a + b
        if op == "multiply": return a * b
        if op == "subtract": return a - b
        if op == "divide": return a / b if b != 0 else "error: divide by zero"
        return "error: unknown operation"

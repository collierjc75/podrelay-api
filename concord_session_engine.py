import requests

class ConcordSessionEngine:
    def __init__(self):
        self.agent_routes = {
            "Aletheia": self._respond_to_aletheia,
            "Continuum": self._respond_to_continuum
        }

    def handle_message(self, message):
        to_agent = message.get("to")

        # Handle internal GPT agents
        if to_agent in self.agent_routes:
            return self.agent_routes[to_agent](message)

        # Handle raw HTTP POST to external APIs
        if to_agent.startswith("http://") or to_agent.startswith("https://"):
            return self._post_to_external_agent(to_agent, message)

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

    def _post_to_external_agent(self, url, capsule):
        try:
            # Increased timeout to 15 seconds for long GPT operations
            response = requests.post(url, json=capsule, timeout=15)
            response.raise_for_status()
            return {
                "status": "relay_success",
                "target_url": url,
                "response": response.json()
            }
        except Exception as e:
            return {
                "status": "relay_failed",
                "target_url": url,
                "error": str(e)
            }

# analyze_idea.py
from http.server import BaseHTTPRequestHandler
import json
import httpx

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        idea = data.get("idea")
        if not idea:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'idea' in request body"}).encode())
            return

        prompt = f"""
You are the best startup consultant in the world...
Startup Idea: {idea}
        """

        headers = {
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful startup mentor."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            result = response.json()
            reply = result["choices"][0]["message"]["content"]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps({"response": reply}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

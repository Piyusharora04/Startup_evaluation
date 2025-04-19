# from http.server import BaseHTTPRequestHandler
# import json
# import httpx

# GROQ_API_KEY = "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"
# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# class handler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         content_length = int(self.headers.get('Content-Length', 0))
#         body = self.rfile.read(content_length)
#         data = json.loads(body)

#         idea = data.get("idea")

#         if not idea:
#             self.send_response(400)
#             self.end_headers()
#             self.wfile.write(json.dumps({"error": "Missing 'idea' in request body"}).encode())
#             return

#         prompt = f"""
# You are the best startup consultant in the world. You have a lot of experience in analyzing startup ideas and providing actionable insights.
# You are given a startup idea and you need to analyze it and provide the following:
# 1. Estimated budget (in INR or USD).
# 2. Steps to build and launch the startup.
# 3. A realistic timeline in months.

# Provide answer in the format 
# 1. Estimated budget: answer...
# 2. Steps to build and launch the startup : answer...
# 3. A realistic timeline in months: answer...
# and do not use any unrequired bullets.

# Startup Idea: {idea}
# """

#         headers = {
#             "Authorization": f"Bearer {GROQ_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "model": "llama-3.3-70b-versatile",
#             "messages": [
#                 {"role": "system", "content": "You are a helpful startup mentor."},
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         try:
#             response = httpx.post(GROQ_API_URL, headers=headers, json=payload)
#             result = response.json()

#             formatted_content = result["choices"][0]["message"]["content"].replace("2. ", "<br><br>2. ").replace("3. ", "<br><br>3. ")

#             self.send_response(200)
#             self.send_header('Content-Type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps({"response": formatted_content}).encode())

#         except Exception as e:
#             self.send_response(500)
#             self.end_headers()
#             self.wfile.write(json.dumps({"error": str(e)}).encode())
            



from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx

app = Flask(__name__)
CORS(app)  # This sets Access-Control-Allow-Origin: * for all routes

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/api/analyze_idea", methods=["POST"])
def analyze_idea():
    data = request.get_json()
    idea = data.get("idea")

    if not idea:
        return jsonify({"error": "Missing 'idea' in request body"}), 400

    prompt = f"""
You are the best startup consultant in the world. You have a lot of experience in analyzing startup ideas and providing actionable insights.
You are given a startup idea and you need to analyze it and provide the following:
1. Estimated budget (in INR or USD).
2. Steps to build and launch the startup.
3. A realistic timeline in months.

Provide answer in the format 
1. Estimated budget: answer...
2. Steps to build and launch the startup : answer...
3. A realistic timeline in months: answer...
and do not use any unrequired bullets.

Startup Idea: {idea}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
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
        response = httpx.post(GROQ_API_URL, headers=headers, json=payload)
        result = response.json()
        formatted_content = result["choices"][0]["message"]["content"].replace("2. ", "<br><br>2. ").replace("3. ", "<br><br>3. ")
        return jsonify({"response": formatted_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required to expose 'app' for Vercel Python runtime
app = app

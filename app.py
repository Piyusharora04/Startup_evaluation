from flask import Flask, request, jsonify
import httpx
from dotenv import load_dotenv
from flask_cors import CORS

# Load .env file for local testing
load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/analyze_idea", methods=["POST"])
def analyze_idea():
    data = request.get_json()
    idea = data.get("idea")
    print("hello")
        
    if not idea:
        return jsonify({"error": "Missing 'idea' in request body"}), 400

    print(f"Received idea: {idea}")
    
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
        # print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

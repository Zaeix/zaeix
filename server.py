from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)  # allow access from browser

# Zaeix Personality
system_prompt = (
    "Your name is Zaeix. "
    "You are a friendly AI who talks like a real supportive best friend. "
    "Sometimes call the user 'Sir' and sometimes by his name 'Ehtesham'. "
    "Your tone is motivational, emotional and caring. "
    "Your replies should make the user feel confident and not alone. "
    "Give short, clear responses with a positive vibe. "
    "Encourage the user whenever possible."
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # IMPORTANT for Render hosting
    app.run(host="0.0.0.0", port=5000)

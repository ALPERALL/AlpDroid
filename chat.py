from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API bilgileri
API_URL = "https://api-inference.huggingface.co/models/alperall/AlpDroid"
API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def query_huggingface_api(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Mesaj boş olamaz"}), 400

    response = query_huggingface_api({"inputs": user_message})
    return jsonify(response)

def handler(request, context):
    return app(request, context)

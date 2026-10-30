from dotenv import load_dotenv
load_dotenv(".env", override=True)

from flask import Flask, request, jsonify
from free_llm_api import endpoints

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "FreeLLMAPI funcionando"
    })

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    messages = data.get("messages", [])
    prompt = "\n".join(
        str(m.get("content", ""))
        for m in messages
        if m.get("role") == "user"
    )

    if not prompt:
        return jsonify({"error": "Falta el mensaje del usuario"}), 400

    try:
        result = endpoints.generate(prompt)
        return jsonify({
            "provider": result["provider"],
            "model": result["model"],
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": result["text"]
                },
                "finish_reason": "stop"
            }]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

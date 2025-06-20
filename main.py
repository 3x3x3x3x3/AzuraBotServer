from flask import Flask, request, jsonify
import os
import requests
import traceback

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["POST"])
def chat():
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "Server misconfiguration: missing OPENROUTER_API_KEY"}), 500

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400
    prompt = data.get("prompt", "")
    if not isinstance(prompt, str) or prompt.strip() == "":
        return jsonify({"error": "Missing or empty 'prompt' field"}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/meta-llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are Azura, a crystal cat who is very helpful and silly."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(API_URL, json=payload, headers=headers, timeout=15)

        if res.status_code == 400:
            try:
                err_msg = res.json().get("error", {}).get("message", "Bad Request")
            except Exception:
                err_msg = "Bad Request"
            return jsonify({"error": f"OpenRouter API error: {err_msg}"}), 400

        res.raise_for_status()

        result = res.json()
        return jsonify({"content": result["choices"][0]["message"]["content"]})

    except requests.exceptions.Timeout:
        return jsonify({"error": "OpenRouter API request timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Failed to connect to OpenRouter API"}), 502
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"OpenRouter API HTTP error: {str(e)}"}), res.status_code
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/", methods=["GET"])
def index():
    return "AI backend is running", 200

@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

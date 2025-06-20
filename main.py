from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def chat():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openrouter/phi-2",  
            "messages": [
                {"role": "system", "content": "You are Azura, a crystal cat who is very helpful and silly."},
                {"role": "user", "content": prompt}
            ]
        }

        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        print("Raw OpenRouter response:", res.text)
        res.raise_for_status()

        result = res.json()
        return jsonify({"content": result["choices"][0]["message"]["content"]})
    
    except Exception as e:
        import traceback
        print("Error occurred:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

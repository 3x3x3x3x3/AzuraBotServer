from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_TOKEN = os.getenv("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", "")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def build_prompt(msg):
    return (
        "Azura is a silly blue crystal cat who talks like a Roblox player.\n"
        "Player: Hi Azura!\n"
        "Azura: Hey there! What’s up?\n"
        f"Player: {msg}\n"
        "Azura:"
    )

@app.route('/azura', methods=['POST'])
def azura():
    data = request.json
    msg = data.get('message', '')
    if not msg:
        return jsonify({'reply': "Say something first!"})
    prompt = build_prompt(msg)
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "do_sample": True,
            "top_k": 50
        }
    }
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        res = response.json()
        if isinstance(res, list) and 'generated_text' in res[0]:
            text = res[0]['generated_text']
            reply = text[len(prompt):].strip().split("\n")[0]
            return jsonify({'reply': reply})
    return jsonify({'reply': "Azura took a nap!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

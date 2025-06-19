from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/azura', methods=['POST'])
def azura():
    data = request.json
    msg = data.get('message', '')
    if not msg:
        return jsonify({'reply': "you didn't say anything 💀"})

    headers = {
        'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
        'messages': [
            {
                'role': 'system',
                'content': "You are Azura, a silly blue crystal cat NPC living inside a Roblox game. You're chaotic, funny, weird, and talk like a Roblox player. Never say you're an AI."
            },
            {'role': 'user', 'content': msg}
        ]
    }

    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=payload
    )
    try:
        reply = response.json()['choices'][0]['message']['content']
    except Exception:
        reply = "azura broke lol"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

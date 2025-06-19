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
        'model': 'gryphe/mythomist-7b',
        'messages': [
            {'role': 'system', 'content': "You are Azura, a blue crystal cat NPC. You are chaotic, weird, silly, and talk like a Roblox player. Never say you're an AI."},
            {'role': 'user', 'content': msg}
        ]
    }

    r = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=payload)
    try:
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "azura broke lol"

    return jsonify({'reply': reply})

app.run(host='0.0.0.0', port=8080)

import os
import requests
from flask import Flask, request, Response

users = []

TELEGRAM_INIT_WEBHOOK_URL = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/{os.getenv("SETWEBHOOK")}/message'

requests.get(TELEGRAM_INIT_WEBHOOK_URL)
app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text == '/start':
        users.append(chat_id)
        send_message(chat_id, "Welcome to our SitSmart system, detection has started...")
    return Response("success")


def send_message(chat_id, text):
    send_url = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.get(send_url, params=payload)


def start_flask_server():
    app.run(port=5002)


if __name__ == "__main__":
    start_flask_server()

import os
import requests
from flask import Flask, request, Response

users = []

API_URL = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/'
TELEGRAM_INIT_WEBHOOK_URL = API_URL + f'{os.getenv("SETWEBHOOK")}/message'


requests.get(TELEGRAM_INIT_WEBHOOK_URL)
app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text == '/start':
        users.append(chat_id)
        send_message(chat_id, "Welcome to our SitSmart system, please choose the number of  your workspace from the "
                              "picture below")
        send_photo(chat_id, open(r'IMG_0443.JPG', 'rb'))
        send_message(chat_id, "")
    return Response("success")


def send_photo(chat_id, file_opened):
    method = 'sendPhoto'
    params = {'chat_id': chat_id}
    files = {'photo': file_opened}
    response = requests.post(API_URL + method, params, files=files)
    return response


def send_message(chat_id, text):
    method = 'sendMessage'
    send_url = API_URL + method
    payload = {'chat_id': chat_id, 'text': text}
    requests.get(send_url, params=payload)


def start_flask_server():
    app.run(port=5002)


if __name__ == "__main__":
    start_flask_server()

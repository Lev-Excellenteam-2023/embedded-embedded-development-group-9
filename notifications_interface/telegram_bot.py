# import os
import requests
from flask import Flask, request, Response
import manager
from Person_Detection import PersonDetection

chat_id_bounding_box_dict = {}
TOKEN = '6413186718:AAHiFecdSbZRKg1rRkxhCbJomP9et4xLBT4'
API_URL = 'https://api.telegram.org/bot6413186718:AAHiFecdSbZRKg1rRkxhCbJomP9et4xLBT4/'
TELEGRAM_INIT_WEBHOOK_URL = API_URL + 'setWebhook?url=https://1f91-62-219-32-82.ngrok-free.app/message'

requests.get(TELEGRAM_INIT_WEBHOOK_URL)
app = Flask(__name__)
in_register_progress = []


@app.route('/message', methods=["POST"])
def handle_message():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text == '/start' and chat_id not in in_register_progress:
        in_register_progress.append(chat_id)
        print("hi")
        image_path, bounding_boxes_dict = PersonDetection()
        send_message(chat_id, "Welcome to our SitSmart system, please choose the number of  your workspace from the "
                              "picture below")
        send_photo(chat_id, open(image_path, 'rb'))
        chat_id_bounding_box_dict[chat_id] = bounding_boxes_dict
    elif message_text.isdigit():
        manager.add_user(chat_id, chat_id_bounding_box_dict[chat_id][int(message_text)])
        send_message(chat_id, "detection has been started...")
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

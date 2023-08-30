import requests
from flask import Flask, request, Response
import manager
from person_detection import person_detection
import users_database
from notifications_interface.telegram_data import TELEGRAM_INIT_WEBHOOK_URL, API_URL, TOKEN
from datetime import datetime

chat_id_bounding_box_dict = {}

requests.get(TELEGRAM_INIT_WEBHOOK_URL)
app = Flask(__name__)
in_register_progress = []
registered_users = []


@app.route('/message', methods=["POST"])
def handle_message():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text == '/start' and chat_id not in in_register_progress:
        in_register_progress.append(chat_id)
        image_path, bounding_boxes_dict = person_detection()
        send_message(chat_id, "Welcome to our SitSmart system, please choose the number of  your workspace from the "
                              "picture below")
        send_photo(chat_id, open(image_path, 'rb'))
        chat_id_bounding_box_dict[chat_id] = bounding_boxes_dict
    elif message_text.isdigit() and chat_id in in_register_progress:
        manager.add_user(chat_id, chat_id_bounding_box_dict[chat_id][int(message_text)])
        send_message(chat_id, "detection has been started...")
        in_register_progress.remove(chat_id)
        registered_users.append(chat_id)
        print(users_database.users)
    elif message_text == '/generate_report' and chat_id in registered_users:
        send_message(chat_id, generate_report(chat_id))
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


def generate_report(chat_id: int):
    report = '\n'.join(users_database.users_reports[chat_id])
    return report


def insert_notification_to_user_report(chat_id: int, text: str):
    report = datetime.now().strftime("%H:%M:%S") + " " + text
    if chat_id in users_database.users_reports.keys():
        users_database.users_reports[chat_id].append(report)
    else:
        users_database.users_reports[chat_id] = [report]


def handle_notification(chat_id, text):
    insert_notification_to_user_report(chat_id, text)
    send_message(chat_id, text)


def start_flask_server():
    app.run(port=5002)


if __name__ == "__main__":
    start_flask_server()

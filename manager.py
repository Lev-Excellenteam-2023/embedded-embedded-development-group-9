import threading
from person_detection import person_detection
from user import User
import users_database
from notifications_interface.telegram_bot import start_flask_server, send_message
from users_database import users
from detect_posture import monitor


def get_workspace_image():
    # gets the image with bounding boxes
    image_path, bounding_box_dict = person_detection()
    return image_path, bounding_box_dict


def add_user(chat_id: int, coordinates: tuple):
    new_user = User(chat_id, coordinates)
    # adding user to user list
    users_database.add_user(new_user)


def main():
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()

    while True:
        for user in users:
            is_bad_posture, message = monitor(user)
        if is_bad_posture:
            send_message(user.chat_id, message)

import threading
from notifications_interface.telegram_bot import start_flask_server, send_message
from users_database import users
from detect_posture import monitor


def main():
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()

    while True:
        for user in users:
            is_bad_posture, message = monitor(user)
            if is_bad_posture:
                send_message(user.chat_id, message)


if __name__ == "__main__":
    main()

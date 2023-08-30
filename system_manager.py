import multiprocessing
from notifications_interface.telegram_bot import start_flask_server, send_message
import users_database
from detect_posture import monitor


def main():
    # Start the Flask server in a separate subprocess
    flask_process = multiprocessing.Process(target=start_flask_server)
    flask_process.start()

    while True:
        users = users_database.get_users()
        if users:
            users_database.detection_started = True
        for user in users:
            is_bad_posture, message = monitor(user)
            if is_bad_posture:
                send_message(user.chat_id, message)


if __name__ == "__main__":
    main()

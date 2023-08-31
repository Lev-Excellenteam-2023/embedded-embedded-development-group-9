import os

from user import User
import json
from json.decoder import JSONDecodeError

latest_frame = None
detection_started = False
filename = r'C:\Users\tamar\excellenteam\bootcamp\raspberryProj\project\users_file.json'
users_reports = {}

# users = []


def add_user(user: User):
    # users.append(user)
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []
    except JSONDecodeError:
        data = []

    for data_user in data:
        if data_user['chat_id'] == user.chat_id:
            return
    data.append(user.to_dict())

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# def get_user(chat_id: int) -> User:
#     for user in users:
#         if user.chat_id == chat_id:
#             return user
#     return None


def get_users() -> list:
    users = []
    if os.path.getsize(filename) == 0:
        return users
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            for user_data in data:
                users.append(User(**user_data))
    except FileNotFoundError:
        pass
    return users


def empty_users():
    with open(filename, 'w') as json_file:
        json_file.truncate(0)  # Truncate the file to remove content


def update_user(user):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    updated_data = []

    for user_data in data:
        if user_data.get("chat_id") == user.chat_id:
            updated_data.append(user.to_dict())
        else:
            updated_data.append(user_data)

    with open(filename, 'w') as json_file:
        json.dump(updated_data, json_file, indent=4)
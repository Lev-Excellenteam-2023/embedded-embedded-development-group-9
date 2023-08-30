from user import User

latest_frame = None
detection_started = False
users = []
users_reports = {}

def add_user(user: User):
    users.append(user)


def get_user(chat_id: int) -> User:
    for user in users:
        if user.chat_id == chat_id:
            return user
    return None


def get_users() -> list:
    return users

from person_detection import person_detection
from user import User
import users_database


def get_workspace_image():
    # gets the image with bounding boxes
    image_path, bounding_box_dict = person_detection()
    return image_path, bounding_box_dict


def add_user(chat_id: int, coordinates: tuple):
    new_user = User(chat_id, coordinates)
    # adding user to user list
    users_database.add_user(new_user)



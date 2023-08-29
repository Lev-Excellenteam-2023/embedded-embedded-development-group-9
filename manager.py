from Person_Detection import PersonDetection
from user import User
import users_database


# global variable of list of users
users = []


def get_workspace_image():
    # gets the image with boundingboxes
    image_path, bounding_box_dict = PersonDetection()
    return image_path, bounding_box_dict


def add_user(chat_id: int, coordinates: tuple):
    new_user = User(chat_id, coordinates)
    # adding user to userlist, (firbase)
    users_database.add_user(new_user)



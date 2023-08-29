from Person_Detection import PersonDetection
from user import User
import data

# global variable of list of users
user = []


def add_user():
    # gets the image with boundingboxes
    imagepath, bounding_box_dict = PersonDetection()
    # TODO function Rivky needs to add that works with the telegram

    # gets user with corresponding boundingbox
    user_id, num = telegram_user(imagepath)
    # TODO integration with Tamari to create a user
    new_user = User(user_id, bounding_box_dict[num])
    #adding user to userlist, (firbase)
    data.add_user(new_user)

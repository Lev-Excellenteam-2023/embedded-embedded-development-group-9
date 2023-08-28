from Person_Detection import PersonDetection

#global variable of list of users
user=[]

def addUser():
    imagepath,bounding_box_dict= PersonDetection()
    #TODO function Rivky needs to add that works with the telegram
    user_id,num=telegram_user(imagepath)
    #TODO integration with Tamari to create a user
    new_user=User(user_id,bounding_box_dict[num])



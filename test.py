import os
def folderCreator():
    CURRENT_DIRECTORY = os.getcwd()
    FOLDER_NAME = input("Please enter the name of the target folder for JSON data under the current directory: " + CURRENT_DIRECTORY + 
    ". \nA new folder of the same name will be automatically created if it does not exist: \n")
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
        print("New folder created: {}/{}".format(CURRENT_DIRECTORY, FOLDER_NAME))
folderCreator()
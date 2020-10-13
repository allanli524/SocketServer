import socket
import json
import threading
import time
from time import gmtime, strftime
import os
HEADER = 1024
FORMAT = "utf-8"
SAVING_INTERVAL = 0
STOP_INTERVAL = 0
FOLDER_NAME = ""
CURRENT_DIRECTORY = ""

while True:
    SAVING_INTERVAL = input("How often do you want to program to save? (seconds)")
    STOP_INTERVAL = input("How long do you want to program to run for? (seconds)")
    if STOP_INTERVAL < SAVING_INTERVAL:
        print("Length of saving interval must be shorter than total program running time.")
    else:
        break

def folderCreator():
    CURRENT_DIRECTORY = os.getcwd()
    FOLDER_NAME = input("Please enter the name of the target folder for JSON data under the current directory: " + CURRENT_DIRECTORY + 
    ". \nA new folder of the same name will be automatically created if it does not exist: \n")
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
        print("New folder created: {}/{}".format(CURRENT_DIRECTORY, FOLDER_NAME))

def start():
    PORT = 1001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER = "192.168.1.67"
    ADDR = (SERVER, PORT)
    s.bind(ADDR)
    s.listen(1)
    print("SERVER_STARTING")
    print(f"SERVER_LISTENING: {SERVER}")
    start_time = time.time()
    system_start_time = time.time()
    content = []


    while True:
        print("[ITERATED]")
        conn, addr = s.accept()
        current_time = time.time()

        elapsed_time = current_time - start_time
        print(elapsed_time)
        
        if elapsed_time > SAVING_INTERVAL and len(content) > 0:
            json_data = json.dumps(content, indent=4, sort_keys=True)
            time_now = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            ADDRESS = '{}/{}/{}.json'.format(CURRENT_DIRECTORY, FOLDER_NAME, time_now)
            newFile = open(ADDRESS, "w+")
            newFile.close()
            outfile = open(ADDRESS, "w")
            outfile.write(json_data)
            print("[WRITTEN]")
            outfile.close()
            content.clear()
            start_time = time.time()
            
        if current_time - system_start_time > STOP_INTERVAL:
            break
        
        connected = True

        while connected:
            msg = conn.recv(HEADER).decode(FORMAT).replace("'", '"')
            if len(msg) > 10:
                content.append(json.loads(msg))
                print("[ITERATION]: " + msg)
                print(len(content))
            else:
                connected = False

    conn.shutdown(1)
    conn.close()
    print("SERVER SHUTDOWN")

folderCreator()
start()
print("PROGRAM IS CLOSING")
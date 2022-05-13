import socket
from datetime import *
from _thread import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate(
    'coe444-446-firebase-adminsdk-kmcfh-7261c8cafd.json')

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://coe444-446-default-rtdb.firebaseio.com/'
})

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection...')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))

    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')

        event = data.decode('utf-8')

        now = datetime.now()

        event_time = now.strftime(" %d %b, %y %H:%M:%S")

        event_info = {
            'info': event,
            'time': event_time
        }

        print(event_info)

        if 'fire' in event:
            ref = db.reference('/FireHistory')
            ref.push(event_info)

        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    print("Connection established")

ServerSocket.close()
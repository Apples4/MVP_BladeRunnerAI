#!/usr/bin/python3

import cv2
import socket
import pickle


"""setting up the socket to recieve the video"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "127.0.0.1"
port = 5000
s.bind((ip, port))

"""Loop for recieveing video from the client"""
while True:
    """Recieve bytes from client"""
    x = s.recvfrom(20000000)
    clientip = x[1][0]
    data = x[0]
    """Load the bytes from the client server"""
    data = pickle.loads(data)
    """Convert the bytes into color video"""
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    """Show the client image"""
    cv2.imshow("Img_Server", img)

    if cv2.waitKey(5) & 0xFF == 27:
        break

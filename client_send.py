#!/usr/bin/python3

import cv2
import socket
import struct
import pickle


def send_video(video_path: str):
    """
    Use socket to make a connection to the server
    
    params:
        video_path: a path to the video

    return:
        sends the video to the server
    """
    if video_path is None or isinstance(video_path, str):
        print("Invalid video path")

    server_ip = "127.0.0.1"
    server_port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    connection = client_socket.makefile("wb") 

    """Opening the video/stream and setting resolution"""
    cap = cv2.VideoCapture(video_path)
    cap.set(3, 640)
    cap.set(4, 480)
    """Looping through the video to stream it"""
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]

    while cap.isOpened():
        """ Looking at the video and returning and store it in img"""
        ret, img = cap.read()
        if not ret:
            print("Error: Could not read frame from video")
            break

        """ encode the video into frames and compress it"""
        results, img = cv2.imencode(".jpg",
                                   img,
                                   encode_param) 
        if not result:
            print("Error: Could not encode frame")
            break
        """Save the buffer as pickle to then sent it as bytes"""
        data = pickle.dumps(img)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)
        """end look after pressing 'q' for 5 seconds"""
        if cv2.waitKey(5) & 0xFF == 27:
            break
    """Close any open leaks"""
    cv2.destroyAllWindows()
    cap.release()

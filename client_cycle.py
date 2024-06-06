#!/usr/bin/python3

import cv2
import os
import time
import socket
import struct
import pickle
from icecream import ic


def send_video(input_video_path: str):
    """Capture video, send it to a server, and receive processed video back.

    Args:
        input_video_path (str): Path to the input video file.

    Returns:
        None
    """
    if input_video_path is None or not isinstance(input_video_path, str):
        print("Invalid input video path")
        return

    # Connect to server
    HOST = "127.0.0.1"
    PORT = 5000
    """HOST = "10.0.0.2"
    PORT = 8000"""
    ic()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ic()
    client_socket.connect((HOST, PORT))
    print("connection made")
    connection = client_socket.makefile('wb')

    # Open video capture
    cam = cv2.VideoCapture(input_video_path)
    cam.set(3, 640)
    cam.set(4, 480)

    # Parameters for JPEG encoding
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break

        # Encode frame as JPEG
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        # Send size and data to server
        client_socket.sendall(struct.pack(">L", size) + data)

        # Receive processed frame size from server
        size = struct.unpack(">L", client_socket.recv(4))[0]
        data = b""

        # Receive processed frame data from server
        while len(data) < size:
            data += client_socket.recv(4096)

        frame_data = data[:size]
        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        frame_path = f"frames/frame_{int(time.time())}.jpg"
        # Display the received frame
        if not os.path.exists('frames'):
            os.makedir('frames')
        cv2.imwrite(frame_path, frame)
        time.sleep(0.1)

    cam.release()
    client_socket.close()
    """cv2.destroyAllWindows()"""


if __name__ == "__main__":
    send_video("video_1.mp4")


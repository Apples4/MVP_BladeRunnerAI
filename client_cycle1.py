#!/usr/bin/python3

import cv2
import time
import socket
import struct
import pickle
from icecream import ic
import logging


logging.basicConfig(level=logging.DEBUG)
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
    RETRY_DELAY = 1
    
    while True:
        try:
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
            logging.info(f"Sending video from {input_video_path}")
            

            while cam.isOpened():
                ret, frame = cam.read()
                if not ret:
                    logging.debug("Connection made")
                    break

                # Encode frame as JPEG
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                data = pickle.dumps(frame, 0)
                ic()
                size = len(data)

                # Send size and data to server
                try:
                    # Send size and data to server
                    client_socket.sendall(struct.pack(">L", size) + data)
                    ack = client_socket.recv(3)
                    if ack != b'ACK':
                        print("Did not receive ACK, closing connection")
                        break
                except ConnectionResetError as e:
                    print(f"Send error: {e}")
                    break 

            cam.release()
            client_socket.close()
            """cv2.destroyAllWindows()"""
            print("Client connection closed")
            break

        except ConnectionRefusedError as e:
            print(f"Connection error: {e}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"Unhandled error: {e}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

if __name__ == "__main__":
    send_video("video_1.mp4")
    print("Client connection closed")

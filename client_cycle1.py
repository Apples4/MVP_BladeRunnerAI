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

    """ client host and port details """
    HOST = "127.0.0.1"
    PORT = 5000
    RETRY_DELAY = 0.25

    """ connect to server, loop to reconnect """
    while True:
        try:
            logging.info("reconnecting")
            client_socket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
            ic()
            client_socket.connect((HOST, PORT))
            logging.info("connection made")
            connection = client_socket.makefile('wb')

            """ Setting up video feed """
            cam = cv2.VideoCapture(input_video_path)
            cam.set(3, 640)
            cam.set(4, 480)

            """ Parameters for JPEG encoding """
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
            logging.info(f"Sending video from {input_video_path}")

            """ Loop to sent the video to server until it ends"""
            while cam.isOpened():
                ret, frame = cam.read()
                if not ret:
                    logging.debug("Connection made")
                    client_socket.sendall(TERMINATION_SIGNAL)
                    break

                """ Encode each frame as JPEG """
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                data = pickle.dumps(frame)
                logging.info("convert frames into bytes")
                size = len(data)

                """ Send size and data to server """
                try:
                    client_socket.sendall(struct.pack(">L", size) + data)
                    logging.debug("Waiting for ACK")
                    ack = client_socket.recv(3)
                    logging.debug(f"Received {ack}")
                    if ack != b'ACK':
                        logging.error("Did not receive ACK, closing connection")
                        break
                except ConnectionResetError as e:
                    logging.error(f"Send error: {e}")
                    break
                
            cam.release()
            client_socket.close()
            logging.info("Client connection closed")
            break
        except ConnectionRefusedError as e:
            a = RETRY_DELAY
            logging.error(f"Connection error: {e}. Retrying in {a} seconds...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            a = RETRY_DELAY
            logging.error(f"Unhandled error: {e}. Retrying in {a} seconds...")
            time.sleep(RETRY_DELAY)


if __name__ == "__main__":
    send_video("video_1.mp4")
    logging.info("Client process finished")

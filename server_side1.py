#!/usr/bin/python3

import cv2
import os
import socket
import struct
import pickle
import numpy as np
import torch
import logging
import time
import icecream as ic
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors


logging.basicConfig(level=logging.DEBUG)
"""class Detection:


    def __init__(self, capture_index):
        self.capture_index = capture_index
        self.model = YOLO("models/best.pt")

        self.annotator = None
        self.start_time = 0
        self.end_time = 0

        self.device = "cuda" if torch.cuda.is_available() else "cpu" """
        
def predict(img):
    """function to run ML model on video

    params:
        img: video data from the user

    returns:
        returns results from the prediction
    """
    logging.debug("Running prediction")
    results = model(img)
    return results

def plot_annotate(results, img):
    """
    function to put annotations onto the stream/ given video

    params:
        results: video data that has been processed by the model
        img: streaming data from the client

    returns:
        returns annotated images from ml
    """
    logging.debug("Annotating frame")
    class_ids = []
    annotator = Annotator(img, 3, results[0].names)
    boxes = results[0].boxes.xyxy.cpu()
    clas = results[0].boxes.cls.cpu().tolist()
    names = results[0].names
    for box, cls in zip(boxes, clas):
        class_ids.append(cls)
        annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
    return img, class_ids

def main():
    """
    private function that uses the above function to 
    process the video stream

    returns:
        returns the processed image to the client
    """

    logging.info("Starting server")
    while True:
        try:
            HOST = ""
            PORT = 5000
            server_socket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET,
                                     socket.SO_REUSEADDR,
                                     1)

            server_socket.bind((HOST, PORT))
            server_socket.listen(10)
            logging.info(f"Server listening on {HOST}:{PORT}")

            while True:
                conn, addr = server_socket.accept()
                logging.info(f"Connection from {addr}")

                data = b""
                payload_size = struct.calcsize(">L")
                
                while len(data) < payload_size:
                    data += conn.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
            
                while len(data) < msg_size:
                    data += conn.recv(4096)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                
                results = predict(img)
                img, class_ids = plot_annotate(results, img)

                frame_filename = f"frame_{int(time.time())}.jpg"
                frame_path = os.path.join("frames", frame_filename)
                cv2.imwrite(frame_path, img)
                cv2.imshow("Frame", img)
                print(f"Frame saved at {frame_path}")

                conn.close()

        except OSError as e:
            if e.errno == 98:
                print("Address already in use, retrying...")
                if server_socket:
                    server_socket.close()
                time.sleep(1)
            else:
                raise e
        finally:
            if server_socket:
                server_socket.close()
    """server_socket.close()"""


if __name__ == "__main__":
    if not os.path.exists('frames'):
        os.makedir('frames')
    main()

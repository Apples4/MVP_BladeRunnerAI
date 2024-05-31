#!/usr/bin/python3

import cv2
import socket
import struct
import pickle
import numpy as np
import torch
from time import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors


class Detection:
    """
    class used to detect objects in a video,
    the model is trained to look at guns and crowbar
    """


    def __init__(self, capture_index):
        """
        Function to initialise instance with camera index

        params:
            capture_index: video path to the video
        """
        self.capture_index = capture_index
        self.model = YOLO("models/best.pt")

        """adding visual information """
        self.annotator = None
        self.start_time = 0
        self.end_time = 0

        """checking if device uses cpu or gpu """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def predict(self, img):
        """function to run ML model on video

        params:
            img: video data from the user

        returns:
            returns results from the prediction
        """
        results = self.model(img)
        return results

    def plot_annotate(self, results, img):
        """
        function to put annotations onto the stream/ given video

        params:
            results: video data that has been processed by the model
            img: streaming data from the client

        returns:
            returns annotated images from ml
        """
        class_ids = []
        self.annotator = Annotator(img, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clas = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        for box, cls in zip(boxes, clas):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
        return img, class_ids

    def __call__(self):
        """
        private function that uses the above function to process the video stream

        returns:
            returns the processed image to the client
        """
        HOST = "127.0.0.1"
        PORT = 5000
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print('Socket now listening')
        conn, addr = server_socket.accept()

        data = b""
        payload_size = struct.calcsize(">L")
        
        frame = 0
        while True:
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
            
            results = self.predict(img)
            img, class_ids = self.plot_annotate(results, img)
            
            result, img = cv2.imencode(".jpg", img)
            
            processed_frame_data = pickle.dumps(img)
            processed_frame_size = len(processed_frame_data)

            conn.sendall(struct.pack(">L", processed_frame_size) + processed_frame_data)

        conn.close()
        server_socket.close()


if __name__ == "__main__":
    detection = Detection(capture_index="video_1.mp4")
    detection()

#!/usr/bin/python3

import cv2
import os
import socket
import struct
import pickle
import numpy as np
import torch
import time
import logging
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors


logging.basicConfig(level=logging.DEBUG)

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

    def handle_client(self, conn):
        """
        function that handles dissconnections between server and client

        params:
            conn: connection between server and client

        returns:
            an error or the data of the client
        """
        try:
            while True:
                data = b""
                payload_size = struct.calcsize(">L")
                
                while len(data) < payload_size:
                   data_chunk = conn.recv(4096) 
                   if not data_chunk:
                       logging.error("No data received")
                       return
                   data += data_chunk

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
            
                while len(data) < msg_size:
                   data_chunk = conn.recv(4096)
                   if not data_chunk:
                       logging.error("Incomplete data received")
                       return
                   data += data_chunk

                frame_data = data[:msg_size]

                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame_path =  "frames/frame.jpg"
                logging.debug("Frame received and decoded")
                cv2.imwrite(frame_path, frame)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                results = self.predict(img)
                img, class_ids = self.plot_annotate(results, img)

                frame_filename = f"frame_{int(time.time())}.jpg"
                frame_path = os.path.join("frames", frame_filename)
                cv2.imwrite(frame_path, img)
                cv2.imshow("Frame", img)
                logging.info(f"Frame saved at {frame_path}")

                conn.sendall(b'ACK')


        except Exception as e:
            logging.error(f"Error processing frame: {e}")
        finally:
            conn.close()
            logging.info("Connection closed")


    def __call__(self):
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
                    self.handle_client(conn)

            except OSError as e:
                if e.errno == 98:
                    logging.error("Address already in use, retrying...")
                    if server_socket:
                        server_socket.close()
                    time.sleep(1)
                else:
                    raise e
            except Exception as e:
                logging.error(f"Unhandled server error: {e}")
                time.sleep(5)
            finally:
                if server_socket:
                    server_socket.close()


if __name__ == "__main__":
    if not os.path.exists('frames'):
        os.makedir('frames')

    detection = Detection(capture_index=0)
    detection()

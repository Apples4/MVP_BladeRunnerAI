#!/usr/bin/python3

import cv2
import socket
import numpy as np


while True:
    try:
        frame_size = int.from_bytes(client_socket.recv(4), byteorder="big")
        if frame_size == 0:
            print("end of video stream")
            break

        img = "b"
        while len(img) < frame_size:
            packet = client_socket.recv(frame_size - len(img))
            if not packet:
                break
            img += packet

        nparr = np.frombuffer(img, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        cv2.imshow("client video stream")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except ConnectionAbortedError:
    print("Correction closed by server")
    break

cv2.destroyAllWindows()
client_socket.close()


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 5000
    client_socket.connect((server_ip, server_port))

#!/usr/bin/python3

import socket
import struct
import pickle
import cv2


"""Main function to receive video from client, process it, and send it back."""
HOST = ""
PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
print("server created")
server_socket.listen(10)
print('Socket now listening')

conn, addr = server_socket.accept()
data = b""
payload_size = struct.calcsize(">L")

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

    # Deserialize frame
    frame = pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Process frame (convert to grayscale)
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    result, processed_frame = cv2.imencode('.jpg', processed_frame)

    # Serialize processed frame
    processed_frame_data = pickle.dumps(processed_frame, 0)
    processed_frame_size = len(processed_frame_data)

    # Send size and data back to client
    conn.sendall(struct.pack(">L", processed_frame_size) + processed_frame_data)

conn.close()
server_socket.close()

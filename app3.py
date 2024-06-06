import subprocess
import os
import cv2
import time
import streamlit as st
from icecream import ic


from streamlit_webrtc import VideoTransformerBase, webrtc_streamer


# Define Video Transformer Class
ic()
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Read the frame from the shared directory
        frame_path = "frames/frame.jpg"
        if os.path.exist(frame_path):
            img = cv2.imread(frame_path)
            return img
        else:
            st.warning("Frames not available et. Waiting ...")
            return frame.to_ndarray(format="bgr24")

# Define Function to Run Server and Client Scripts
def run_server_and_client():
    # Run server_side2.py in a subprocess
    server_process = subprocess.Popen(["python3", "server_side2.py"])

    # Run client_cycle1.py in a subprocess
    client_process = subprocess.Popen(["python3", "client_cycle1.py"])
    return server_process, client_process


# Run Streamlit App and Server/Client Scripts
if __name__ == "__main__":
    st.title("Streamlit WebRTC App")

    # Start server and client processes
    server_process, client_process = run_server_and_client() 
    frame_path = "frames/frame.jpg"
    while not os.path.exists(frame_path):
            st.warning("Frames not available yet. Waiting...")
            time.sleep(2)

    # Run Streamlit app
    webrtc_streamer(key="example",
                    video_transformer_factory=VideoTransformer)

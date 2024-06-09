import os
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2

frame_dir = "frames"  # Directory where frames are saved by server_side2.py

def video_frame_callback(frame):
    # Get the latest frame from the directory
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    if not frame_files:
        return frame
    
    # Create a new VideoFrame from the ndarray
    return av.VideoFrame.from_ndarray(frame, format="rgb24")

if __name__ == "__main__":
    st.title("WebRTC Video Streamer Example")

    webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDONLY,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True}
    )

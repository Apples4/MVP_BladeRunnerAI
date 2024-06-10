import streamlit as st
from save_to_csv import save_info
from data_base.save_to_main_frame import update_main
import pandas as pd
import numpy as np
import os
import time
import cv2
import subprocess

os.environ["KMP_DUPLICATE_LIB_OK"]="True"

# Remove frames when app ends
def cleanup_frames():
    # Define directories to delete
    directories = ["frames/camera1", "frames/camera2"]

    # Loop through directories and delete contents
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            st.info(f"Deleted contents of directory: {directory}")
        else:
            st.warning(f"Directory does not exist: {directory}")

# start server and client
def server_start():
    server_process_1 = subprocess.Popen(["python3", "server_1.py"])
    server_process_2 = subprocess.Popen(["python3", "server_2.py"])

def client_start():
    client_process_1 = subprocess.Popen(["python3", "client_1.py"])
    client_process_2 = subprocess.Popen(["python3", "client_2.py"])

# Setting up streamlit app
st.set_page_config(
    page_title="BladeRunnerAI",
    page_icon="OIG4.jpg",
)

st.title("BladeRunnerAI :skull_and_crossbones:")
st.markdown("Home Page")

server_start()
client_start()
save_info("video_2.mp4")
# updating main data for detection
update_main("output.csv", "data_base/main_dectection_data.csv")
# Dividing page into two columns for
# camera and notification history

# Notification side
with st.sidebar:
    st.header("Notifications")
    df = pd.read_csv("output.csv")
    df = df[["confidence", "class_name"]]
    st.dataframe(df, hide_index=True)
# Camera or video display """
st.header("Video Feed")
tab1, tab2 = st.tabs(["Camera 1", "Camera 2"])
def display_frames(tab_header, frames_dir):
    tab_header.header(tab_header.title)
    def get_frame_files():
        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')], 
                             key=lambda x: os.path.getmtime(os.path.join(frames_dir, x)))
        return frame_files

    frame_placeholder = st.empty()
    displayed_frames = set()

    while True:
       # Get the list of frames
        frame_files = get_frame_files()

        for frame_file in frame_files:
            if frame_file not in displayed_frames:
                # Read and display the frame
                frame_path = os.path.join(frames_dir, frame_file)
                img = cv2.imread(frame_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(img, channels="RGB")
                    displayed_frames.add(frame_file)
                    # Wait before showing the next frame
                    time.sleep(0.01)

        # Wait for a short period before checking for new frames
        time.sleep(0.15)

# Tab 1
with tab1:
    tab1.title = "Camera 1"
    display_frames(tab1, "frames/camera1")

# Tab 2
with tab2:
    tab2.title = "Camera 2"
    display_frames(tab2, "frames/camera2")

if __name__ == "__main__":
    display_frames(tab1, "frames/camera1")
    display_frames(tab2, "frames/camera2")

    st.experimental_set_query_params(cleanup=True)
    if "cleanup" in st.experimental_get_query_params():
        cleanup_frames()

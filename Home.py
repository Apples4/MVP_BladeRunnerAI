import streamlit as st
from save_to_csv import save_info
from data_base.save_to_main_frame import update_main
import pandas as pd
import numpy as np
import os
import time
import cv2
import subprocess

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


# Remove frames when app ends
def cleanup_frames():
    """
    function to delete frames after the streamlit app closes

    returns:
        Nothing, deletes frames in folders
    """
    # Define directories to delete
    directories = ["frames/camera1", "frames/camera2"]

    # Loop through directories and delete contents
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            st.info(f"Deleted contents of directory: {directory}")
        else:
            st.warning(f"Directory does not exist: {directory}")

# start server and client


def server_start():
    """
    function to start server script accepts connection then recieve
    video from client for the server to process the frames
    """
    server_process_1 = subprocess.Popen(["python3", "server_1.py"])
    server_process_2 = subprocess.Popen(["python3", "server_2.py"])


def client_start():
    """
    function to start client script send connection then sends
    video to client for the server to process the frames
    """
    client_process_1 = subprocess.Popen(["python3", "client_1.py"])
    client_process_2 = subprocess.Popen(["python3", "client_2.py"])


# Setting up streamlit app
st.set_page_config(
    page_title="BladeRunnerAI",
    page_icon="OIG4.jpg",
)

st.title("BladeRunnerAI :skull_and_crossbones:")
st.markdown("Home Page")

# Starting server and client
server_start()
client_start()
save_info("video_2.mp4")
# updating main data for detection
update_main("output.csv", "data_base/main_dectection_data.csv")
# Dividing page into two columns for
# camera and notification history

# Show current detections side
with st.sidebar:
    st.header("Current Detections")
    df = pd.read_csv("output.csv")
    df = df[["confidence", "class_name"]]
    st.dataframe(df, hide_index=True)
# Camera or video display
st.header("Video Feed")
tab1, tab2 = st.tabs(["Camera 1", "Camera 2"])

# Tab 1
with tab1:
    tab1.title = "Camera 1"

    # Create a placeholder in the Streamlit app

    def display_frames_camera1():
        # function to show frames in tab0

        def get_frame_files():
            """
            function to sort .jpg images in a particular order

            returns:
                frame_files: sorted frames
            """
            frames_dir = "frames/camera1"
            frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')],
                                 key=lambda x: os.path.getmtime(os.path.join(frames_dir, x)))
            return frame_files

        # place holder for fram using streamlit
        frame_placeholder = st.empty()
        displayed_frames = set()

        # loop to check for new frames and show new frames
        while True:
            frame_files = get_frame_files()
            # loop the frames and place it in app
            for frame_file in frame_files:
                if frame_file not in displayed_frames:
                    frame_path = os.path.join("frames/camera1", frame_file)
                    # reading the image using cv1
                    img = cv2.imread(frame_path)
                    if img is not None:
                        frame_placeholder.image(img, channels="RGB")
                        displayed_frames.add(frame_file)
                        # rate at which frames are shown
                        time.sleep(0.5)

            time.sleep(0.5)

    display_frames_camera1()

# Tab 2
with tab2:
    tab2.title = "Camera 2"
    # Create a placeholder in tab2

    def display_frames_camera2():
        # function to display frames in tab"
        def get_frame_files():
            frames_dir = "frames/camera2"
            frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')],
                                 key=lambda x: os.path.getmtime(os.path.join(frames_dir, x)))
            return frame_files

        # place holder for fram using streamlit
        frame_placeholder = st.empty()
        displayed_frames = set()

        # loop to check for new frames and show new frames
        while True:
            frame_files = get_frame_files()

            # loop through frames in the folder
            for frame_file in frame_files:
                if frame_file not in displayed_frames:
                    frame_path = os.path.join("frames/camera2", frame_file)
                    # reading the image using cv2
                    img = cv2.imread(frame_path)
                    if img is not None:
                        frame_placeholder.image(img, channels="RGB")
                        displayed_frames.add(frame_file)
                        # rate at which frames are shown
                        time.sleep(0.5)
            # rate at checking the ne
            time.sleep(0.5)

    display_frames_camera2()


if __name__ == "__main__":
    cleanup_frames()
    # remove temp files
    os.remove("output.csv")

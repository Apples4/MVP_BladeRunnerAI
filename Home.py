import streamlit as st
from detection_cv import process_frame
from save_to_csv import save_info
from data_base.save_to_main_frame import update_main
import pandas as pd
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="True"


# Setting up streamlit app
st.set_page_config(
    page_title="BladeRunnerAI",
    page_icon="OIG4.jpg",
)

st.title("BladeRunnerAI :skull_and_crossbones:")
st.markdown("Home Page")

save_info("video_1.mp4")
# updating main data for detection
update_main("output.csv", "data_base/main_dectection_data.csv")
# Dividing page into two columns for
# camera and notification history

col1, col2, = st.columns([0.3, 0.7], gap="large")
# Notification side """
with col1:
    st.header("Notifications")
    df = pd.read_csv("output.csv")
    df = df[["confidence", "class_name"]]
    st.dataframe(df, hide_index=True)
# Camera or video display """
with col2:
    st.header("Video Input")
    tab1, tab2, tab3 = st.tabs(["Camera 1",
                                "Camera 2",
                                "Camera 3"])

    with tab1:
       st.header("Camera 1")
       processed_video = process_frame("video_1.mp4")
       video_file = open("output_video.mp4", "rb")
       video_bytes = video_file.read()
       st.video(video_bytes, start_time=10)

    with tab2:
       st.header("Camera 2")
       video_file = open('video_2.mp4', 'rb')
       video_bytes = video_file.read()
       st.video(video_bytes, start_time=10)

    with tab3:
       st.header("Camera 3")
       video_file = open('video_1.mp4', 'rb')
       video_bytes = video_file.read()
       st.video(video_bytes, start_time=10)

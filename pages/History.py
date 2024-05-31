import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(                                                             
    page_title="BladeRunnerAI",
    page_icon="OIG4.jpg",  
)
st.title("BladeRunnerAI")

st.markdown("History of all detections that have happened")

# spliting Notification page

col1, col2, = st.columns([0.7, 0.3], gap="large")

# Graph of notification
with col1:
    st.header("Notification Timeline")
    # Making the graph
    df = pd.read_csv("data_base/main_dectection_data.csv")
    data = df[["class_name", "counts"]]
    st.bar_chart(data=data,
                 x="class_name",
                 y="counts",
                 color=None,
                 width=0,
                 height=0,
                 use_container_width=True)

with col2:
    st.header("Notifiation History")
    st.dataframe(data)

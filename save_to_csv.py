#!/usr/bin/python3

import supervision as sv
from ultralytics import YOLO
from datetime import datetime
import pandas as pd


model = YOLO("models/best.pt")


def save_info(input_video_path: str):
    """
    This funcition saves detection information

    params:
        input_video_path: path to the video
    return:
        cvs file names "output.csv"
    """
    frames_generator = sv.get_video_frames_generator(input_video_path)
    with sv.CSVSink() as sink:
        """ loop through the frames """
        for frame_index, frame in enumerate(frames_generator):
            results = model(frame)[0]
            detections = sv.Detections.from_ultralytics(results)
            sink.append(detections, {"time": datetime.now})
            break

    df = pd.read_csv("output.csv")
    """ Display the DataFrame with the specified columns """
    (df[["time", "class_name", "confidence"]])
    df.to_csv("output.csv", index=False)

#!/usr/bin/python3

import numpy as np
import supervision as sv
from ultralytics import YOLO
import time


def process_frame(input_video_path: str):
    """

    params:
        input_video_path: string to video to process

    Returns:
        processed video
    """
    model = YOLO("yolov8n.pt")
    tracker = sv.ByteTrack()
    box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    def callback(frame: np.ndarray, _: int) -> np.ndarray:
        results = model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = tracker.update_with_detections(detections)

        labels = [
            model.model.names[class_id]
            for class_id
            in detections.class_id
        ]

        annotated_frame = box_annotator.annotate(
            frame.copy(), detections=detections)
        return label_annotator.annotate(
            annotated_frame, detections=detections, labels=labels)

    sv.process_video(
        source_path=input_video_path,
        target_path="output_video.mp4",
        callback=callback
    )

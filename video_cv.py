#!/usr/bin/python3

import cv2


def create_video_frames(video_path):
    """
    function opens a video file, reads each frame,
    converts the color of the frame,
    and stores all frames in a list

    params:
        video_path: link or path to the video
    Returns:
        Stores frams in a list
    """
    frames = []

    cap = cv2.VideoCapture(video_path)

    """ Find OpenCV version"""
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = cap.get(cvs.CAP_PROP_FPS)
    
    """ reading the number of frames in the video """
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        finally:
            cap.release()
            return frames, fps

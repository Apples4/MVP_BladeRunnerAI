#MVP-BladeRunnerAI

This is a MVP for a BladeRunnerAI idea, which used computer vision for perhome and company security. It is in essence using CCTV camera footage and machine learning models to detect potentially harmful around the premises.

To run this streamlit app [Home.py], the required libraries need to be installed, look at the requirements.txt. The app streams a video from the client to the server, the server then runs a object detection model using YOLO model on each frame.

These frames are saved in the frames/camera1 and frames/camera2 folders. There is a function in the streamlit app, which plays the frames on a localhost so it appears to stream the frames as they are processed in realtime.

----------
install necessary libraries:
```
$ pip install -r requirements.txt
```
to run app:
```
$ python3 streamlit run Home.py
```
The password to unlock the app is "streamlit123"


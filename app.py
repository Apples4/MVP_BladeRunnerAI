import dash
import time
from dash import dcc, html
from dash.dependencies import Input, Output
import os
from flask import Flask, send_file
import threading
from client_cycle import send_video
from server_side import Detection
import subprocess


# Define the Flask server
server = Flask(__name__)

# Define the Dash app
app = dash.Dash(__name__, server=server)

# Define the Dash app layout
app.layout = html.Div([
    html.H1("Video Stream"),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
    html.Img(id='video-frame')
])

@app.callback(
    Output('video-frame', 'src'),
    Input('interval-component', 'n_intervals')
)
def update_frame(n):
    frame_files = sorted(os.listdir("frames"),
                         key=lambda x: int(x.split('_')[1].split('.')[0]))
    if frame_files:
        latest_frame = frame_files[-1]
        return f"/frames/{latest_frame}"
    return "/frames/frame_0.jpg"

@server.route('/frames/<filename>')
def serve_frame(filename):
    return send_file(os.path.join("frames", filename), mimetype='image/jpeg')

# Function to run the Flask app in a separate thread
def run_flask_app():
    server.run(host='127.0.0.1', port=5001)

# Function to run server-side and client-side scripts
def run_server_and_client():
    server_process = subprocess.Popen(["python3",
                                       "server_side.py"])
    time.sleep(5)
    client_process = subprocess.Popen(["python3",
                                       "client_cycle.py",
                                       "video_1.mp4"])
    return server_process, client_process

if __name__ == "__main__":
    # Run the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Run the server-side and client-side scripts
    server_process, client_process = run_server_and_client()

    # Run the Dash app
    app.run_server(debug=True)

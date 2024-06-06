from shiny import App, ui, reactive
from flask import Flask, send_file
import threading
import subprocess
import os
import glob
import time
import logging


logging.basicConfig(level=logging.DEBUG)

def run_server_and_client():
    logging.info("Starting server and client")
    server_process = subprocess.Popen(["python3", "server_side2.py"])
    client_process = subprocess.Popen(["python3", "client_cycle1.py", "video_1.mp4"])
    return server_process, client_process

app_ui = ui.page_fluid(
    ui.h1("Video Stream"),
    ui.img(id="video-frame", src="/frames/frame.jpg"),
    ui.tags.script(
        """
        setInterval(function(){
          var image = document.getElementById('video-frame');
          var currentSrc = image.src;
          var nextSrc = '/frames/' + (parseInt(currentSrc.match(/frame_(\\d+).jpg/)[1]) + 1) + '.jpg';
          image.src = nextSrc;
        }, 1000);
        """
    )
)

flask_app = Flask(__name__)

@flask_app.route("/frames/<filename>")
def serve_frame(filename):
    frame_path = os.path.join("frames", filename)
    if os.path.exists(frame_path):
        return send_file(frame_path, mimetype="image/jpeg")
    else:
        return "Frame not found", 404

def run_flask_app():
    flask_app.run(host="127.0.0.1", port=5001)

def server(input, output, session):
    @reactive.Effect
    def _():
        ui.output_image("video-frame", "frames/frame.jpg")

app = App(app_ui, server)


if __name__ == "__main__":
    if not os.path.exists('frames'):
        os.makedirs('frames')
    
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    logging.info("Flask app started")
    server_process, client_process = run_server_and_client()
    logging.info("Server and client started")
    app.run()

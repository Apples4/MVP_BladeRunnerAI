from shiny import App, ui, render
from flask import Flask, send_file
from client_cycle import send_video
from server_side import Detection
import threading
import subprocess
import os


app_ui = ui.page_fluid(
        ui.h1("Video Stream"),
        ui.img(id="video-frame", scr="/frames/frame.jpg"),
        ui.tags.script(
        """
        setInterval(function(){
          document.getElementById('video-frame').src = '/frames/frame.jpg?' + new Date().getTime();
        }, 1000);
        """
    )
)

flask_app = Flask(__name__)
def server(input, output, session):
    @reactive.Effect
    def _():
        ui.output_image("video_frame", "recieved_frames/frame.jpg")

app = App(app_ui, server)

@flask_app.route("/frames/<filename>")
def run_flask_app():
    flask_app.run(host="127.0.0.1", port=5001)


def serve_frame(filename):
    return send_file(os.path.join("recived_frames", filename), mimetype="image/jpeg")

def run_server_and_client():
    server_process = subprocess.Popen(["python3", "server_side.py"])
    client_process = subprocess.Popen(["python3", "client_cycle.py", "video_1.py"])
    return server_process, client_process


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    server_process, client_process = run_server_and_client()

    app.run()

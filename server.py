from datetime import datetime
from flask import Flask
from flask import render_template
from flask import Response
from cv2 import *

app = Flask(__name__)


@app.route("/")
def main():
    time_str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('main.html', time=time_str)


def gen():
    cam = VideoCapture(0)
    while True:
        cam_opened, img = cam.read()

        if cam_opened:
            imwrite("a.jpg", img)
            # cam.release()
        frame = open('a.jpg', 'rb').read()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.debug = True
app.run(host = '0.0.0.0',port=80)


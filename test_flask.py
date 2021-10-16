import json
from flask import Flask, render_template
from camera_handler import CameraHandler

app = Flask(__name__)
camera = CameraHandler()

@app.route('/')
def index_handler():
    return render_template('index.html')


@app.route('/liveview')
def liveview_handler():
    #camera.get_liveview()
    return render_template('liveview.html')

@app.route('/last_liveview_picture')
def last_liveview_handler():
    return camera.get_last_liveview_picture()

@app.route('/take_a_photo')
def take_a_photo_handler():
    if camera.ready:
        res = camera.get_one_picture()['result'][0][0]
        return render_template('one_photo.html', photo_path=res)
    else:
        return "Haudi Ho"


@app.route('/gallerie')
def gallerie_handler():
    return render_template('gallerie.html')


if __name__ == '__main__':
    app.run(debug=True)

from libsonyapi.camera import Camera, ConnectionError
from libsonyapi.actions import Actions
import json
import atexit
from PIL import Image
import requests
import threading
import liveview_parser


class CameraHandler:

    def __init__(self):
        atexit.register(self.shoot_down)
        try:
            self._camera = Camera()
        except ConnectionError:
            self._camera = None  # todo: show error on display
        self._ready = False
        self._liveview_mode = False
        self._liveview_thread = None
        if self._camera is not None:
            print("Camera ready", self._camera)  # todo: remove print -> message on display
            self._ready = True

    def get_camera(self):
        return self._camera

    @property
    def ready(self):
        return self._ready

    def get_one_picture(self):
        res = self._camera.do(Actions.actTakePicture)
        if res.get('result') is not None:
            self._live_mode_off()
            photo_path = res['result'][0][0]
            photo_name = photo_path.split('/')[-1]
            im = Image.open(requests.get(photo_path, stream=True).raw)
            im.save('images/' + photo_name)  # todo: directory must be before start and liveview directory

        return res
    def _live_mode_off(self):
        if self._liveview_mode:
            self._camera.do(Actions.stopLiveview)
            self._liveview_mode = False

    def get_liveview(self):
        if self.ready:
            self._live_mode_off()
            res = self._camera.do(Actions.startLiveview)
            self._liveview_mode = True
            liveview_path = res['result'][0]
            print(liveview_path)
            self._liveview_thread = threading.Thread(target=self._liveview_thread_loop, args=[liveview_path])
            self._liveview_thread.start()

    def _liveview_thread_loop(self, liveview_path):
        liveview_parser.start_liveview(liveview_path)

    def get_last_liveview_picture(self):
        return liveview_parser.get_last_liveview_picture()

    def shoot_down(self):
        if self.ready:
            self._live_mode_off()
            self._camera.do(Actions.stopRecMode)


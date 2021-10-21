from libsonyapi.camera import Camera, ConnectionError
from libsonyapi.actions import Actions
from PIL import Image
import requests
import threading
import liveview_parser


class CameraHandler:

    def __init__(self):
        try:
            self._camera = Camera()
        except ConnectionError:
            self._camera = None  # todo: show error on display
            print("Camera unavailable")
        self._ready = False
        self._liveview_mode = False
        self._liveview_thread = None
        self._mode_photo_immediately = True
        if self._camera is not None:
            print("Camera ready", self._camera)  # todo: remove print -> message on display
            self._ready = True

    def get_camera(self):
        return self._camera

    @property
    def ready(self):
        return self._ready

    def get_one_picture(self):
        if self._liveview_mode:
            self.stop_liveview()
        if self._mode_photo_immediately:
            return self._make_picture_immediately()
        else:
            return self._make_picture_delayed()

    def start_liveview(self):
        if self.ready:
            self.stop_liveview()
            res = self._camera.do(Actions.startLiveview)
            if res.get('result') is not None:
                self._liveview_mode = True
                liveview_path = res['result'][0]
                self._liveview_thread = threading.Thread(target=self._liveview_thread_loop, args=[liveview_path])
                self._liveview_thread.start()
                return True
            return False

    def get_last_liveview_picture(self):
        """

        :return: True if picture is saved False if not
        """
        return liveview_parser.get_last_picture()

    def stop_liveview(self):
        if liveview_parser.is_on_run():
            liveview_parser.stop_liveview()
        if self._liveview_mode:
            self._camera.do(Actions.stopLiveview)
            self._liveview_mode = False

    def _liveview_thread_loop(self, liveview_path):
        liveview_parser.start_liveview(liveview_path)

    def _make_picture_immediately(self):
        res = self._camera.do(Actions.actTakePicture)
        return self._get_picture_by_path(res)

    def _make_picture_delayed(self):
        res = self._camera.do(Actions.setSelfTimer, param=[2])
        res = self._camera.do(Actions.actTakePicture)
        return self._get_picture_by_path(res)

    def _get_picture_by_path(self, res):
        """
        Take and Save Picture by Path from res
        :param res: result from Camera.Action
        :return: Picture Name or None
        """
        if res.get('result') is not None:
            photo_path = res['result'][0][0]
            photo_name = photo_path.split('/')[-1]
            im = Image.open(requests.get(photo_path, stream=True).raw)
            im.save('images/' + photo_name)  # todo: directory must be before start and liveview directory
            return 'images/' + photo_name  # todo: change 'images' to variable name
        return None

    def shoot_down(self):
        if self.ready:
            self.stop_liveview()
            self._camera.do(Actions.stopRecMode)


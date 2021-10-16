from io import BytesIO

from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.image import Image, CoreImage
from kivy.clock import Clock

from camera_handler import CameraHandler



class PhotoBoxApp(App):

    def __init__(self, camera_handler):
        super(PhotoBoxApp, self).__init__()
        self.camera = camera_handler
        self.counter = 0

    def build(self):
        pass

    def on_start(self):
        img = self.root.ids['liveview_image']
        img.source = 'static/img/accept-47587_640.png'

    def take_a_photo(self):
        if self.camera.ready:
            img_name = self.camera.get_one_picture()
            img = self.root.ids['liveview_image']
            img.source = img_name
        else:
            img = self.root.ids['liveview_image']
            img.source = 'static/img/stop-sign-35069_640.png'

    def on_new_picture_liveview(self, image):
        image.seek(0)
        im = CoreImage(BytesIO(image.read()), ext='png')
        self.root.ids['liveview_image'].texture = im.texture
        # self.root.ids['liveview_image'].reload()

    def start_liveview(self):

        self.root.ids['liveview_image'].source = 'static/liveview/liveview.jpg'
        # self.root.ids['liveview_image'].source = 'static/img/gear-47203_640.png'
        # Clock.schedule_interval(self.on_new_picture_liveview, 0.5)
        self.camera.get_liveview(self.on_new_picture_liveview)

    def show_gallery(self):
        img = self.root.ids['liveview_image']
        img.source = 'static/img/digital-camera-33879_640.png'


if __name__ == '__main__':
    cam = CameraHandler()
    pb = PhotoBoxApp(cam)
    pb.run()

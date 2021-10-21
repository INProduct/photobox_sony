import os
import printing
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

from camera_handler import CameraHandler


class ImageButton(ButtonBehavior, Image):
    pass


class GalleryItem(ButtonBehavior, RelativeLayout):
    pass


class PhotoGui(BoxLayout):
    pass


class PhotoBoxGuiApp(App):

    def __init__(self):
        super(PhotoBoxGuiApp, self).__init__()
        self.camera_handler = CameraHandler()
        self._photo_width = 800
        self._photo_delay = 0

    def on_start(self):
        self.root.sm.current = 'main'
        self._set_camera_available(self.camera_handler.ready)

    def on_stop(self):
        self._stop_liveview()
        self.camera_handler.shoot_down()

    def build(self):
        return PhotoGui()

    def take_a_picture(self, immediately=False):
        if not immediately:
            delay = self.root.sm.screens[0].ids.delay_slider.delay_slider.value
            delay = int(delay)
            if delay == 0:
                self.take_a_picture(immediately=True)
            elif 11 > delay > 0:
                self._photo_delay = delay
                Clock.schedule_once(self._set_countdown)
        else:
            self._stop_liveview()
            res = self.camera_handler.get_one_picture()
            if res is not None:
                self.root.sm.screens[0].liveview_image.source = res
                Clock.schedule_once(self._start_liveview, 5)
            else:
                pass  # todo: error handling picture can't be taken

    def _set_countdown(self, t=None):
        if self._photo_delay == 0:
            self.take_a_picture(immediately=True)
        else:
            self._photo_delay -= 1
            if 0 < self._photo_delay < 6:
                self.root.sm.screens[0].countdown_numbers.size_hint_y = 1
                self.root.sm.screens[0].countdown_numbers.source = 'static/img/movie_' + str(self._photo_delay) + '.png'
            elif self._photo_delay == 0:
                self.root.sm.screens[0].countdown_numbers.size_hint_y = 0
            Clock.schedule_once(self._set_countdown, 1)

    def _set_camera_available(self, val):
        if val:
            self.root.sm.screens[0].liveview_image.source = 'static/img/accept-47587_640.png'
            self.root.sm.screens[0].shoot_button.disabled = False
            self._start_liveview(None)
        else:
            self.root.sm.screens[0].liveview_image.source = 'static/img/stop-sign-35069_640.png'
            self.root.sm.screens[0].shoot_button.disabled = True

    def _start_liveview(self, t):
        res = self.camera_handler.start_liveview()
        if res:
            self.root.sm.screens[0].liveview_image.source = 'static/liveview/liveview.jpg'
            Clock.schedule_interval(self._show_liveview_image, 0.015)
        else:
            pass  # todo: implement error handling

    def _stop_liveview(self):
        Clock.unschedule(self._show_liveview_image)
        self.camera_handler.stop_liveview()

    def _show_liveview_image(self, t):
        res = self.camera_handler.get_last_liveview_picture()
        if res:
            self.root.sm.screens[0].liveview_image.reload()

    def _prepare_gallery(self):
        all_images = os.listdir('images')
        all_images.reverse()
        for img in all_images:
            if img.lower().endswith('jpg'):
                g_item = GalleryItem()
                g_item.gallery_image.source = 'images/'+img
                self.root.sm.screens[1].gallery_container.add_widget(g_item)
                self.root.sm.screens[1].gallery_container.width = self._photo_width * len(all_images)

    def _unload_gallery(self):
        self.root.sm.screens[1].gallery_container.clear_widgets()

    def print_photo(self, path):
        printing.print_image(path)

    def remove_image(self, path):
        try:
            os.remove(path)
        except:
            pass  # todo: error handling
        self.go_to_gallery()

    def go_to_main(self):
        self.root.sm.current = 'main'

    def go_to_gallery(self):
        self._prepare_gallery()
        self.root.sm.current = 'gallery'

    def go_to_detail(self, path):
        self.root.sm.current = 'detail'
        self.root.sm.screens[2].detail_image.source = path


if __name__ == '__main__':
    PhotoBoxGuiApp().run()

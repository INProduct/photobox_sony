import requests
import io
from PIL import Image, UnidentifiedImageError
from queue import Queue


class ImageInformation:

    def __init__(self):
        self.start_byte = 1
        self.payload_type = 1
        self.sequence_number = 2
        self.time_stamp =4

        self.start_code = 4
        self.payload_size = 3
        self.padding_size = 1

    def decode_common_header(self, header):
        self.start_byte = header[:1]
        self.payload_type = header[1:2]
        self.sequence_number = header[2:4]
        self.time_stamp = header[4:]

    def decode_payload_header(self, header):
        self.start_code = header[:4]
        self.payload_size = int.from_bytes(header[4:7], byteorder='big')
        self.padding_size = int.from_bytes(header[7:], byteorder='big')

    def decode_image(self, bytes):
        im_raw_bytes = io.BytesIO(bytes)
        try:
            im = Image.open(im_raw_bytes)  # todo: try catch don't forget
            picturesQueue.put(im)
        except UnidentifiedImageError as e:
            print("Error: ", e)


picturesQueue = None
can_run = False


def is_on_run():
    return can_run


def get_last_picture():
    if picturesQueue is not None:
        im = picturesQueue.get()
        im.save('static/liveview/liveview.jpg')
        return True
    return False


def start_liveview(url):
    global can_run
    global picturesQueue
    can_run = True
    picturesQueue = Queue(maxsize=25)
    r = requests.get(url, stream=True)
    while can_run:
        ii = ImageInformation()
        common_header = r.raw.read(8)
        ii.decode_common_header(common_header)
        payload_header = r.raw.read(128)
        ii.decode_payload_header(payload_header)
        img_bytes = r.raw.read(ii.payload_size)
        offset_bytes = r.raw.read(ii.padding_size)
        ii.decode_image(img_bytes)
    r.close()


def stop_liveview():
    global can_run
    can_run = False

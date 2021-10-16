import datetime
import os

import requests
import io
import queue
from PIL import Image


class ImageInformation:
    work_queue = queue.LifoQueue(maxsize=20)
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
        im = Image.open(io.BytesIO(bytes))
        image_name = 'static/liveview/liveview_' + str(datetime.datetime.timestamp(datetime.datetime.now())) + '.jpg'
        im.save(image_name)
        ImageInformation.work_queue.put(image_name)
        if ImageInformation.work_queue.qsize() > 15:
            os.remove(ImageInformation.work_queue.get())


def get_last_liveview_picture():
    return ImageInformation.work_queue.get()


def start_liveview(url):
    r = requests.get(url, stream=True)
    while True:
        ii = ImageInformation()
        common_header = r.raw.read(8)
        ii.decode_common_header(common_header)
        payload_header = r.raw.read(128)
        ii.decode_payload_header(payload_header)
        img_bytes = r.raw.read(ii.payload_size)
        offset_bytes = r.raw.read(ii.padding_size)
        ii.decode_image(img_bytes)



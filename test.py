from libsonyapi.camera import Camera
from libsonyapi.actions import Actions
import time

camera = Camera()  # create camera instance
camera_info = camera.info()  # get camera camera_info
print(camera_info)

print(camera.name)  # print name of camera
print(camera.api_version)  # print api version of camera

time.sleep(2)

res = camera.do(Actions.actTakePicture)  # take a picture
print("Result", res)

time.sleep(5)

res = camera.do(Actions.startLiveview)
print("Liveview", res)

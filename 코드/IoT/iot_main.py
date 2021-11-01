from threading import Lock
import cv2

from camera import Camera
from stream_camera_device import PiCameraDevice
from config import Config

c_lock = Lock()
camera = cv2.VideoCapture(0)

MQTT_HOST = '192.168.137.222'

if __name__ == '__main__':
    cam = Camera(camera, c_lock, MQTT_HOST)
    PiCameraDevice(Config.device_id, camera, c_lock)
    
    cam.start()

    cam.camera.release()
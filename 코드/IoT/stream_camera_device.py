# from  picamera import PiCamera
from net_device import NetDevice
from threading import Thread, Lock
import io
from socket import *
from config import Config
import cv2

class PiCameraDevice(NetDevice):
    def __init__(self, id, camera, lock):
        # self.camera = cv2.VideoCapture(0)
        self.camera = camera
        super().__init__(id, 'CAMERA')

        # self.camera.resolution = (640, 480)
        # self.camera.framerate = 24
        # self.camera.vflip = True       
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

        self.state = False
        self.lock = lock

    def stream(self, host, port):
        try:
            with socket(type= SOCK_DGRAM) as s:
                # stream = io.BytesIO()
                while self.state:    
                     # UDP 패킷의 최대 크기는 65K, 
                     # PiCamera의 이미지가 이보다 작게 되도록 QUALITY 설정 중요
                     # snapshot과 self.camera 사용 경쟁
                    self.lock.acquire()

                    ret, stream = self.camera.read()
                    result, stream = cv2.imencode('.jpg', stream, self.encode_param)
                     # self.camera.capture(stream, 'jpeg', use_video_port=True, quality=20, resize=(640, 480))
                    
                    self.lock.release()

                    jpgimage = stream.tobytes()
                     # jpgimage = stream.getvalue()

                    s.sendto(jpgimage, (host, port))

                     # stream.seek(0)
                     # stream.truncate()

        except Exception as e:
            print('stream 중단')
            print(e)

    

    def on_start_stream(self, host, port):
        if not self.state:
            self.state = True
            # 스트림 전송은 새로운 스레드로 진행
            Thread(target=self.stream, args=(host, port)).start()

    def on_stop_stream(self):
        self.state = False

    def on_snapshot(self):
        stream = io.BytesIO()
        # stream과 self.camera 사용 경쟁
        # self.lock.acquire()
        self.camera.capture(stream, 'jpeg', use_video_port=True)
        # self.lock.release()
        data = stream.getvalue()
        print(len(data))
        self.send_packet(data)
 
# cam = cv2.VideoCapture(0)
# l = Lock() 
# PiCameraDevice(Config.device_id, cam, l)
        
# from signal import pause
# pause()

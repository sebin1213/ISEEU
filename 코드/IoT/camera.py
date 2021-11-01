import cv2
import time
import os
import datetime
from threading import Thread
from queue import Queue
import shutil

from gpiozero import DistanceSensor
import paho.mqtt.client as mqtt

from send_to_s3 import SendToS3

class Camera:
    def __init__(self, camera, lock, mqtt_host):
        self.data = None
        self.timestamp = None

        # openCV 카메라
        self.cam = camera
        self.frame_size = (int(self.cam.get(3)), int(self.cam.get(4)))

        # 초음파센서
        self.state = False
        self.ultra = DistanceSensor(23, 24, max_distance=1)
        self.threshold_distacne = 0.4
        
        # 동영상 녹화
        self.recording = False
        self.video_queue = Queue()
        self.fc = 20.0
        # self.codec = cv2.VideoWriter_fourcc(*'MP4V')
        self.codec = cv2.VideoWriter_fourcc(*'XVID')

        # 얼굴 크롭
        self.cropping = False
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.crop_count = 0

        # 스레드 관련
        self.lock = lock

        # MQTT
        self.host = mqtt_host # 라즈베리파이 주소 (자기 자신)
        self.port = 1883 # mqtt 포트
        self.topic = 'iseeu/startAI'

        self.client = mqtt.Client()
        self.client.connect(self.host, self.port)

        # boto3
        self.s = SendToS3('yangjae-team03-s3')
        self.key = 'IO-Record-Video/'

    # 스트리밍 함수
    # def stream(self):
    #     # streaming thread 함수
    #     def streaming():
    #         # 실제 thread 되는 함수
    #         self.ret = True
    #         while self.ret:
    #             self.ret, np_image = self.cam.read()
    #             if np_image is None:
    #                 continue
                
    #             self.data = np_image
                
    #             # return np_image

    #     Thread(target=streaming).start()


    # 동영상 녹화 함수
    def record_video(self):
        print('recording')

        # timestamp =  = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'./videos/{self.timestamp}.avi'
        
        while os.path.exists(filename):
            filename = f'./videos/{self.timestamp}.avi'

        out = cv2.VideoWriter(filename, self.codec, self.fc, self.frame_size)

        while self.recording:

            self.lock.acquire()

            ret, frame = self.cam.read()

            self.lock.release()

            if ret:
                out.write(frame)
                self.video_queue.put_nowait(filename)

        self.s.send(filename, self.key+self.timestamp+'.avi')
    

    # 얼굴 크롭 함수
    def make_cropped_face(self):
        print('start make crop')

        start_time = time.time()

        shutil.rmtree("./crop")
        os.mkdir("./crop")

        time.sleep(1)

        while (self.cropping) and (self.crop_count < 15):
            #if time.time() > start_time + 10:
                #print('time over')
                #reak

            self.lock.acquire()

            ret, frame = self.cam.read()

            self.lock.release()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cropped_face = None

            # 얼굴 검출
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:

                cropped_face = frame[int(y):int(y+h),int(x):int(x+h)].copy()

                self.crop_count += 1
                cv2.imwrite('./crop/crop' + str(self.crop_count) + '.jpg', cropped_face)
                time.sleep(0.2)
            
        self.client.publish(self.topic, self.timestamp)
        print('make crop done')

        self.crop_count = 0
        # self.publish()
        
    def publish(self): 
        time.sleep(0.1)

        print('make crop done')

    # 시작 (무한 루프)
    def start(self):
        while True:
            time.sleep(0.05)

            # 스트리밍
            # frame = self.data
            # if frame is not None:
            #     # cv2.imshow('SMS', frame)
            #     print(len(frame))
            #     # 스트리밍을 위해 client에 data 전송
            
            if self.ultra.distance <= self.threshold_distacne:
                # ai에게 데이터 전송 (mqtt 운영)
                #

                # print('motion detected!')
                if self.state == False:
                    # print('work thread start ============================================================')
                    self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

                    self.recording = not self.recording
                    self.cropping = not self.cropping

                    # 동영상 녹화 스레드 운영
                    if self.recording:
                        t_record_video = Thread(target=self.record_video)
                        t_record_video.start()
                    
                    # 얼굴 크롭 스레드 운영
                    if self.cropping:
                        t_make_crop = Thread(target=self.make_cropped_face)
                        t_make_crop.start()

                self.state = True
                
                time.sleep(15)
            
            else:   
                print('no motion')    
                if self.state == True:                    
                    self.recording = not self.recording
                    self.cropping = not self.cropping
                    # self.publish()
                
                self.state = False
                
     
    def __del__(self):
        self.cam.release()

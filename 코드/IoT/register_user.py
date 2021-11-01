import paho.mqtt.client as mqtt
import os
import cv2
import time
from send_to_s3 import SendToS3

class Register:
    def __init__(self, host, port, forever=True):
        self.host = host
        self.port = port

        self.client = mqtt.Client()
        self.forever = forever
        self.topic = 'iseeu/register'
        self.msg = ""

        # self.cam = cv2.VideoCapture(0)

        # 얼굴 크롭
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        self.count = 0

        self.s = SendToS3('yangjae-team03-s3')
        self.filename = ""

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code', rc)
        if rc == 0:
            client.subscribe(self.topic, 2) # 연결 성공 시 토픽 구독 신청
        else:
            print('연결 실패 : ', rc)
    

    def on_message(self, client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        
        if msg.topic == self.topic:
            self.msg = msg.payload.decode()
            print('start make crop')
            self.make_user_crop()

    def make_user_crop(self):
        self.cam = cv2.VideoCapture(0)
        # user_id = len(os.walk('/home/pi/iot_workspace/iseeu_ai/iseeu_ai/user').next()[2]) + 1
        # user_id = len(os.listdir('/home/pi/iot_workspace/iseeu_ai/iseeu_ai/user')) + 1
        user_id = len(os.listdir('/home/pi/iot_workspace/iseeu_ai/iseeu_ai/user')) + 1
        print(user_id)
        time.sleep(0.5)

        while self.count < 1:
            ret, frame = self.cam.read()
            time.sleep(0.5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cropped_face = None

            # 얼굴 검출
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:

                cropped_face = frame[int(y):int(y+h),int(x):int(x+h)].copy()

                self.filename = f"{str(user_id)}_user_{self.msg}.jpg"

                print('-----------------------------', self.filename)
                self.count += 1
                cv2.imwrite('./user/' + self.filename, cropped_face)
                print("finish write")
            
        
        self.count = 0
        frame = None
        self.cam.release()

        self.publish()
        print("-----------------done---------------")

        # time.sleep(1)
        # self.s.send(self.filename, "Registered-User/" + self.filename)

    def upload(self):
        pass

    def publish(self):
        self.client.publish('iseeu/work', 'done')

    def start(self):

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port)

        if self.forever:
            self.client.loop_forever()
        else:
            self.client.loop_start()

HOST = "54.176.66.35"
PORT = 1883

if __name__ == '__main__':
    r = Register(HOST, PORT)
    r.start()
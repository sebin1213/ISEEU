import paho.mqtt.client as mqtt
import datetime
import threading

from iseeu_ai import IseeUAI
from send_to_s3 import SendToS3

class Subscribe:
    def __init__(self, i, s, host, port, topic, forever=True):
        self.i = i
        self.s = s

        self.host = host
        self.port = port

        self.topic = topic
        self.message = ''
        self.forever = forever

        self.client = mqtt.Client()

        self.state = False

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code', rc)
        if rc == 0:
            client.subscribe(self.topic, 2) # 연결 성공 시 토픽 구독 신청
        else:
            print('연결 실패 : ', rc)
    
    def start_ai(self):
        # AI 동작
        self.i.make_person_list(self.i.unknown_face_path, 'unknown')
        self.i.make_person_list(self.i.crop_face_path, 'crop')

        print("\n------------예측 시작 (user)-----------")
        predict_start_time = datetime.datetime.now()
        target, person_id = self.i.predict('user')
        predict_end_time = datetime.datetime.now()
        print("------------예측 완료 (user)-----------")

        print("\n예측하는데 걸린 시간 (user) : ", predict_end_time-predict_start_time)
        print()

        # user에서 예측 성공
        if person_id != -1:
            key = self.i.image_record_write(target, person_id, self.message)

            file_name = f"./record/{key}"
            key = 'IO-Record/' + key
            # res = s3.upload_file(file_name, bucket, key)
            self.s.send(file_name, key)

        # user에 원하는 결과 없음 -> unknown으로 넘어감
        else:
            print("\n------------예측 시작 (unknown)-----------")
            predict_start_time = datetime.datetime.now()
            target, person_id = self.i.predict('unknown')
            predict_end_time = datetime.datetime.now()
            print("------------예측 완료 (unknown)-----------")

            print("\n예측하는데 걸린 시간 (unknown) : ", predict_end_time-predict_start_time)
            print()

            # unknown 에서 예측 성공
            if person_id != -1:
                key = self.i.image_record_write(target, person_id, self.message)
                print('### 분석 결과와 기록된 시간 :',key) 
                file_name = f"./record/{key}"
                key = 'IO-Record/' + key
                # res = s3.upload_file(file_name, bucket, key)
                self.s.send(file_name, key)

            # 완전한 새로운 인물 -> unknown에 새로 등록
            else:
                key_unknown, key_record = self.i.new_unknown_image_record_write(self.message)
                # print('result :',key_unknown)
                print('### 분석 결과와 기록된 시간 : ',key_record)
                # 명단 등록
                file_name = f"./unknown/{key_unknown}"
                key_unknown = 'UnRegistered-User/' + key_unknown
                # res = s3.upload_file(file_name, bucket, key_unknown)
                self.s.send(file_name, key_unknown)

                # 기록 등록
                file_name = f"./record/{key_record}"
                key_record = 'IO-Record/' + key_record
                # res = s3.upload_file(file_name, bucket, key_record)
                self.s.send(file_name, key_record)


        self.i.crop_dict = {}
        self.i.crop_img = []

        self.i.unknown_dict = {}
        self.i.unknown_img = []
        
        self.state = False

        print('\nPredict Done\n\n')

    def on_message(self, client, userdata, msg):
        self.message = msg.payload.decode()

        print(f"Received '{self.message}' from '{msg.topic}' topic")
        # if msg.topic == 'iseeu/startAI':

        if self.state == False:
            print('AI 판별 시작')
            self.state = True
            threading.Thread(target=self.start_ai, daemon=True).start()
        else:
            print('지금은 할 수 없음')
            print(self.state)

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port)

        if self.forever:
            self.client.loop_forever()
        else:
            self.client.loop_start()


HOST = '192.168.137.222' # 라즈베리파이 (자기 자신)
PORT = 1883
TOPIC = 'iseeu/startAI'


if __name__ == "__main__":
    sub = Subscribe(HOST, PORT, TOPIC)
    sub.start()
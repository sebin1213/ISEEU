import warnings
warnings.filterwarnings('ignore')

from iseeu_ai import IseeUAI
from send_to_s3 import SendToS3

from subscribe import Subscribe

# AI 모델 인스턴스
i = IseeUAI()

# S3 전송 인스턴스
bucket = 'yangjae-team03-s3'
s = SendToS3(bucket)

HOST = '192.168.137.222' # 라즈베리파이 (자기 자신)
PORT = 1883
TOPIC = 'iseeu/startAI'

# MQTT Subscribe 인스턴스
sub = Subscribe(i, s, HOST, PORT, TOPIC)

if __name__ == '__main__':
    sub.start()

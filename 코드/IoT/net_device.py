from threading import Thread
from net import NetFile
import json
from time import sleep
from socket import *
from config import Config

class NetDevice(NetFile, Thread):
    def __init__(self, id, dtype):
        NetFile.__init__(self)
        Thread.__init__(self)
        self.setDaemon(True)
        self.id = id
        self.type = dtype
        self.start()

    def run(self):
        self.connect(Config.host)
        while True:
            try:
                msg = self.read_json()
                self.control(msg)
            except ConnectionResetError as e:
                self.reconnect(2)
            except Exception as e:
                print(e.__class__)

    def connect(self, svr=Config.host, port=Config.port):
        super().connect(svr, port)
        # 접속 성공시 id 전송
        self.send_json({
            'cmd': 'join',
            'id': self.id,
            'dtype' : self.type
        })

    def on_ping(self) :
        self.sendline('pong')

    def control(self, msg):
        print(msg)
        cmd = msg.get('cmd')
        kwargs = msg.get('kwargs', {})
        try:            
            method = getattr(self, 'on_' + cmd)
            method(**kwargs)            
        except Exception as e:
            print(e)
            print(f'{self.id} received unknown command {cmd}')



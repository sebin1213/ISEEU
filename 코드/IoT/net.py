from socket import socket
import struct
from time import sleep
import json

class NetFile:
    def __init__(self, socket=None):
        if socket :
            self.socket = socket
            self.reader = self.socket.makefile('rb')
            self.writer = self.socket.makefile('wb')
        else:
            self.socket = None
            self.reader = None
            self.writer = None

    def connect(self, svrip, port):
        self.svrip = svrip
        self.port = port
        self.socket = socket()
        print('try connect', self.svrip, self.port)
        self.socket.connect((self.svrip, self.port))
        self.reader = self.socket.makefile('rb')
        self.writer = self.socket.makefile('wb')
        print('connected')

    def reconnect(self, delay=5):
        self.socket.close()
        while True:
            sleep(delay)
            try:
                print('try reconnect', self.svrip, self.port)
                self.connect(self.svrip, self.port)
                return
            except Exception as e:
                print('reconnect error', e)

    def disconnect(self):
        self.socket.close()
        self.socket = None
        self.reader = None
        self.writer = None

    def send_packet(self, data):
        self.writer.write(struct.pack('<L', len(data)))
        self.writer.flush()
        self.writer.write(data)
        self.writer.flush()

    def read_packet(self):
        data = self.reader.read(struct.calcsize('<L'))
        data_len = struct.unpack('<L', data)[0]
        data = self.reader.read(data_len)
        return data_len, data

    def sendline(self, data):
        self.writer.write(f'{data}\n'.encode())
        self.writer.flush()

    def readline(self):
        return self.reader.readline().decode().strip()

    def send_json(self, msg):
        msg = json.dumps(msg)
        self.sendline(msg)

    def read_json(self):
        msg = self.readline()
        return json.loads(msg)
        

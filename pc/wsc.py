import socketio
import time

class WSC:
    def __init__(self):
        sio = socketio.Client()
        self.ping = None
        @sio.event
        def connect():
            print('connection established sussecc')
            self.ready = 1

        @sio.event
        def disconnect():
            print('disconnected from server')
            self.ready = 0

        @sio.event
        def ping(data):
            #print('ping ', data)
            if self.ping != None:
                self.ping.pong(data)

        self.ready = 0
        self.sio = sio

    def connect(self,url):
        self.sio.connect(url)

    def disconnect(self):
        self.sio.disconnect()

    def send(self,topic,data):
        if self.ready == 1:
            self.sio.emit(topic,data)

    def setPing(self,ping):
        self.ping = ping

if __name__ == '__main__':
    wsc = WSC()
    print("connect to server")
    #wsc.connect('http://127.0.0.1:12306')
    wsc.connect('http://192.168.31.204:12306')

    if wsc.ready == 0:
        time.sleep(5)
    wsc.send('ctrl',{'up':1, 'down':0, 'left':0, 'right':0})
    wsc.send('ctrl', {'up': 1, 'down': 0, 'left': 0, 'right': 0})
    wsc.send('ctrl', {'up': 1, 'down': 0, 'left': 0, 'right': 0})

    time.sleep(5)
    wsc.disconnect()
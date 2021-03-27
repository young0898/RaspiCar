import math
import time
import threading

class Ping(threading.Thread):
    def __init__(self, wsc):
        threading.Thread.__init__(self)
        self.wsc = wsc
        self.delaytime = 0
        self.lastTime = 0
        self.id = 0
        self.finishId = 0
        self.dt = 0

    def run(self):
        while True:
            self.id += 1
            self.lastTime = time.time()
            self.wsc.send('ping',{'id':self.id})
            #print('ping',self.id)
            time.sleep(1)

    def pong(self,data):
        #print('pong',self.id)
        if data['id'] == self.id :
            self.delaytime = (time.time() - self.lastTime) * 1000 #毫秒
            self.finishId = data['id']
            #self.dt = round((time.time() * 1000) - data['time'])
            #print(self.delaytime)

    def getDt(self):
        if self.id > self.finishId + 1:
            return '>1000'
        return math.floor(self.delaytime)  #向下取整

    def getRaspiTime(self):
        return (time.time() * 1000) + self.dt
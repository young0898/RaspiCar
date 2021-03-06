import cv2
import sys
import time
import math
import threading
import numpy as np

class Camera(threading.Thread):
    def __init__(self, server_ip='127.0.0.1'):
        threading.Thread.__init__(self)
        self.serverIp = server_ip
        self.isQuit = False
        self.frame = np.zeros(480*640*3).reshape(480, 640, 3)
        self.fps = 0.0
        
        # 用于计算一个粗略的fps
        self.lastTime = 0
        self.lastFrameCount = 0
        self.camera = None

    def getStatus(self):
        if self.camera == None:
            return -1
        if self.camera.isOpened() == False:
            return -2
        return 0

    # 获取到了一帧的时候调用，用于计算粗略的帧速率，不准，但是可以接受 
    def gotAFrame(self):
        if self.lastTime == 0 :
            self.lastTime = time.time()
        
        self.lastFrameCount += 1

        now = time.time()
        if now - self.lastTime > 1 :
            count = self.lastFrameCount
            t = now - self.lastTime
            self.fps = round(count/t)

            self.lastTime = now
            self.lastFrameCount = 0

    def run(self):
        try:
            while self.isQuit == False:
                try:
                    # print('try 2 connect rtsp')
                    #camera = cv2.VideoCapture(0)
                    camera = cv2.VideoCapture("tcp://%s:12305" % self.serverIp)
                    self.camera = camera
                except Exception as e:
                    print('Error:', e)
                    self.camera = None
                    time.sleep(1)
                    continue
                print('camera connection established success')

                while self.isQuit == False:
                    if camera.isOpened():
                        success,frame = camera.read()
                        if success==False:
                            print('camera read err!')
                            time.sleep(1)
                            break
                        self.frame = frame
                        # print(self.frame.shape)
                        self.gotAFrame()
                    else:
                        print('camera not open!')
                        time.sleep(1)
                        break

                camera.release()
        except KeyboardInterrupt:
                self.isQuit = True
                print('received an ^C and exit.')

if __name__ == '__main__':
    camera = Camera()
    camera.start()
   
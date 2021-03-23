import cv2
import numpy
import socket
import struct
import time


def display_camera_frame():
    server_address = ('192.168.31.61', 12305)
    buffSize = 65535

    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #创建socket对象
    server.bind(server_address)
    print('now waiting for frames...')

    lastTime = 0.0
    lastFrameCount = 0
    while True:
        if lastTime == 0:
            lastTime = time.time()
        lastFrameCount += 1
        nowtime = time.time()
        if nowtime - lastTime > 1:
            fps = round((lastFrameCount / (nowtime - lastTime)), 2)
            print(fps, lastFrameCount)
            lastTime = nowtime
            lastFrameCount = 0

        data, address = server.recvfrom(buffSize) #接收编码图像数据
        data = numpy.array(bytearray(data))  #格式转换
        imgdecode = cv2.imdecode(data,1)  #解码
        imgdecode = imgdecode[::-1, ::-1, :]  #翻转图像
        cv2.imshow('test5',imgdecode) #窗口显示

        if cv2.waitKey(1) == 27: #按下“ESC”退出
            break

    server.close()
    cv2.destroyAllWindows()

if __name__ =='__main__':
    display_camera_frame()
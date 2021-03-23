import socket
import cv2
import numpy as np
import time

def display_camera_frame():
    #sever_address = ('192.168.3.101', 12305)
    sever_address = ('192.168.31.204', 12305)
    #sever_address = ('129.204.4.69', 12305)

    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM代表基于TCP的流式socket通信
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connect to server [%s:%d]" % (sever_address[0], sever_address[1]))
    try:
        s.connect(sever_address)
    except socket.error:
        print("Fail to connect to server")
        exit(0)
 
    print("Connect success")

    while True:
        time_start = time.time() * 1000

        lStr = s.recv(4)
        if len(lStr) != 4:
            print('continue')
            continue

        lenght = int.from_bytes(lStr, 'big')  #图片编码后的长度

        #分片接收图片编码后的内容
        data = bytes([])
        while lenght > 0:
            d = s.recv(lenght)
            data += d
            lenght -= len(d)
        #print(len(data))

        img_array = np.asarray(bytearray(data), dtype = np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  #解码图片
        frame = frame[::-1, ::-1, :]  #翻转图片
        cv2.imshow("video", frame)

        if cv2.waitKey(1) == 27:  # 按下“ESC”退出
            break
        time_end = time.time() * 1000
        print(round(time_end - time_start))

    cv2.destroyAllWindows()
    s.close()

if __name__ =='__main__':
    display_camera_frame()
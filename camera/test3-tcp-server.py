import socket
import cv2
import time
import numpy as np
import sys
import os

def get_ip():
    wlan_ip = os.popen("ifconfig wlan0 | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    eth_ip = os.popen("ifconfig eth0 | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    lo_ip = os.popen("ifconfig lo | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    if wlan_ip is not None:
        return wlan_ip
    elif eth_ip is not None:
        return eth_ip
    else:
        return lo_ip

def start_camera():
    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM代表基于TCP的流式socket通信
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 设置地址与端口，如果是接收任意ip对本服务器的连接，地址栏可空，但端口必须设置
    server_address = ('', 12306)
    sock.bind(server_address)  # 将Socket（套接字）绑定到地址

    try:
        sock.listen(1)   # 监听TCP传入连接
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)

    camera = cv2.VideoCapture(0)  #打开摄像头
    print('分辨率：{} x {}   fps：{}'.format(
        round(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        round(camera.get(cv2.CAP_PROP_POS_FRAMES))))

    while True:
        print("[listen] server address [%s:%d], waiting for connection" % (get_ip(), server_address[1]))
        client, addr = sock.accept()
        print("[connect] client address： [%s:%d]" % (addr[0], addr[1]))

        while camera.isOpened():
            success, frame = camera.read()
            data = cv2.imencode('.jpg', frame)[1]
            lenght = len(data).to_bytes(4, byteorder='big')

            try:
                client.send(lenght)  #发送图片编码后的长度
                client.send(data)    #发送图片编码的内容
            except socket.error as e:
                print("fail info: %s" % e)
                print("[disconnect] remote ip is %s,port is " % addr[0], addr[1])
                break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_camera()

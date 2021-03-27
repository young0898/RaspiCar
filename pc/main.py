# -*- coding: utf-8 -*-
import json
from wsc import WSC
import time
from keyboard_control import Keyboard_Control
from ctrl import Ctrl
from camera import Camera
from display import Display
from ping import Ping
from usb_control import Usb_Control

if __name__ =='__main__':
    wsc = WSC()   #创建wsc
    wsc.connect('http://192.168.31.203:12306')   #连接树莓派

    time.sleep(1)   # 这里应该是异步回调，图省事先

    usbControl = Usb_Control(wsc)
    usbControl.start()

    ctrl = Ctrl(wsc)      #创建控制现场
    ctrl.restartCamera()  # 下发指令给树莓派启动摄像头

    camera = Camera()
    camera.start()

    keyboardControl = Keyboard_Control(wsc)
    keyboardControl.start()

    ping = Ping(wsc)  # 创建ping对象
    ping.start()  # 循环下发ping测指令给树莓派
    wsc.setPing(ping)  # 将ping对象传递给wsc

    display = Display(camera, keyboardControl, ping)
    display.start()



    
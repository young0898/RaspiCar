# -*- coding: utf-8 -*-
import usb.core
import usb.util
import time
import threading

class Usb_Control(threading.Thread):
    def __init__(self, wsc):
        threading.Thread.__init__(self)
        self.wsc = wsc
        self.last_direction = 90
        self.dev = usb.core.find(idVendor= 0x1781, idProduct= 0x0898)
        if self.dev is None:
            #raise ValueError('Device not found')
            print('Device not found')
        else:
            #print(self.dev)
            print('usbControl connection established success')
            self.dev.set_configuration()

    def run(self):
        while self.dev:
            try:
                RCdata = self.dev.read(0x81, 8)
                # print(data)
                '''
                print('CH1: ' + str(RCdata[0]) + '  ' +
                      'CH2: ' + str(RCdata[2]) + '  ' +
                      'CH3: ' + str(RCdata[3]) + '  ' +
                      'CH4: ' + str(RCdata[4]))
                '''
                if RCdata[0]:
                    direction = round(RCdata[0] / 255 * 180)
                    if self.last_direction != direction:
                        self.sendRaw({'direction': direction})
                    self.last_direction = direction

            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue

    def sendRaw(self, data):
        if 'direction' not in data:
            data['direction'] = 90  #方向复位
        self.wsc.send('ctrlRaw', data)
        print('direction:', str(data['direction']))

if __name__ == '__main__':
    usbControl = Usb_Control('')
    usbControl.start()
    #time.sleep(0.05)


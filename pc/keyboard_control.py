# -*- coding: utf-8 -*-
import sys
import keyboard
import fileinput
import time
# 这个只能放在主线程，不阻塞
class Keyboard_Control:
    def __init__(self, wsc):
        self.ctrl0 = {'up':0,'down':0,'left':0,'right':0}
        self.ctrl = {'up':0,'down':0,'left':0,'right':0}
        self.wsc = wsc

    def status(self):
        return self.ctrl

    def start(self):
        def callback(event):
            if event.event_type == 'down':
                if event.name == 'up':
                    self.ctrl['up'] = 1
                if event.name == 'down' :
                    self.ctrl['down'] = 1
                if event.name == 'left' :
                    self.ctrl['left'] = 1
                if event.name == 'right' :
                    self.ctrl['right'] = 1
                    
            if event.event_type == 'up':
                if event.name == 'up':
                    self.ctrl['up'] = 0
                if event.name == 'down':
                    self.ctrl['down'] = 0
                if event.name == 'left':
                    self.ctrl['left'] = 0
                if event.name == 'right':
                    self.ctrl['right'] = 0
            
            if self.ctrl0['up'] != self.ctrl['up'] :
                self.ctrl0['up'] = self.ctrl['up']
                if self.ctrl['up'] == 1 :
                    self.sendRaw({'ch':'up','status':'high'})
                else :
                    self.sendRaw({'ch':'up','status':'low'})
            if self.ctrl0['down'] != self.ctrl['down'] :
                self.ctrl0['down'] = self.ctrl['down']
                if self.ctrl['down'] == 1 :
                    self.sendRaw({'ch':'down','status':'high'})
                else :
                    self.sendRaw({'ch':'down','status':'low'})




            if self.ctrl0['left'] != self.ctrl['left']:
                self.ctrl0['left'] = self.ctrl['left']
                if self.ctrl['left'] == 1 :
                    self.sendRaw({'direction':20})
                else :
                    self.sendRaw({'direction':90})

            if self.ctrl0['right'] != self.ctrl['right']:
                self.ctrl0['right'] = self.ctrl['right']
                if self.ctrl['right'] == 1 :
                    self.sendRaw({'direction':160})
                else :
                    self.sendRaw({'direction':90})

                
        keyboard.on_press(callback, suppress = True)
        keyboard.on_release(callback)

    def sendRaw(self, data):
        if 'direction' not in data:
            data['direction'] = 90  #方向复位
        self.wsc.send('ctrlRaw', data)
        print('direction:', str(data['direction']))

if __name__ == '__main__':
    keyboardControl = Keyboard_Control('')
    keyboardControl.start()
    time.sleep(30)


# -*- coding: utf-8 -*-

class Ctrl:
    def __init__(self, wsc):
        self.wsc = wsc
    
    def restartCamera(self):
        self.wsc.send('exec',{'cmd':'pkill raspivid'})
        self.wsc.send('exec',{'cmd':'raspivid --profile high -l -o tcp://0.0.0.0:12305 -hf -vf -t 0 -w 720 -h 480 -fps 40 &'})

    def openCamera(self):
        self.wsc.send('exec',{'cmd':'raspivid --profile high -l -o tcp://0.0.0.0:12305 -hf -vf -t 0 -w 640 -h 480 -fps 40 &'})

    def closeCamera(self):
        self.wsc.send('exec',{'cmd':'pkill raspivid'})

    def initCarControl(self):
        self.wsc.send('init', {'speed': 112, 'direction': 90})
import os

class Control_Function:
    def __init__(self):
        pass

    def execute(self, cmd):
        os.system(cmd)

    def openCamera(self):
        cmd = "raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 15 &"
        self.execute(cmd)

    def closeCamera(self):
        self.execute("pkill raspivid")

if __name__ == '__main__':
    functionControl = Function_Control()    # 功能控制（开关灯、开关摄像头....）
    #functionControl.openCamera()
    functionControl.closeCamera()
    
import os


class Control_Function:
    def __init__(self):
        pass

    def initWebServer(self):
        cmd = "ps -aux |grep python3 | head -n1 | grep http.server | awk '{print$2}' | xargs -r kill -9"
        self.execute(cmd)
        cmd = "python3 -m http.server 8080 &"
        self.execute(cmd)
        print('初始化web服务')

    def initFlask(self):
        cmd = "ps -aux |grep python3 | head -n1 | grep flask_webServer | awk '{print$2}' | xargs -r kill -9"
        self.execute(cmd)
        cmd = "python3 flask_webServer.py &"
        self.execute(cmd)
        print('初始化Flask web服务')

    def openWebServer(self):
        cmd = "python3 -m http.server 8080 &"
        self.execute(cmd)
        print('开启web服务')

    def closeWebServer(self):
        cmd = "ps -aux |grep python3 | head -n1 | grep http.server | awk '{print$2}' | xargs -r kill -9"
        self.execute(cmd)
        print('关闭web服务')



    def execute(self, cmd):
        os.system(cmd)

    def openCamera(self):
        cmd = "raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 40 &"
        self.execute(cmd)

    def closeCamera(self):
        self.execute("pkill raspivid")

if __name__ == '__main__':
    functionControl = Control_Function()    # 功能控制（开关灯、开关摄像头....）
    #functionControl.openCamera()
    functionControl.closeCamera()
    
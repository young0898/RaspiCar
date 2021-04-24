from flask import Flask, render_template, Response
import cv2
import get_ip
import threading
import numpy as np
import time
import sys

class VideoCamera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 30)
        self.frame = np.ones(480 * 640 * 3).reshape(480, 640, 3)
        self.camera_flag = True

    def __del__(self):
        self.video.release()

    def run(self):
        while self.camera_flag:
            try:
                success, image = self.video.read()
                if success:
                    image = image[::-1, ::-1, :]  # 翻转图片
                    # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
                    ret, frame = cv2.imencode('.jpg', image)
                    #self.frame = frame
                    self.frame = frame.tobytes()
                    #print(time.time()*1000, "put_frame")

            except KeyboardInterrupt:
                print('received an ^C and exit.')
                self.camera_flag = False
                #sys.exit(0)



def gen(camera):
    while camera.camera_flag:
        #print(time.time()*1000,"get_frame------->")
        time.sleep(0.035)
        frame = camera.frame
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__)
camera = VideoCamera()
camera.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_start')  # 这个地址返回视频流响应
def video_start():
    print('startVideo')
    camera.camera_flag = True
    print(camera.camera_flag)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stop')
def video_stop():
    print('stopVideo')
    #camera.camera_flag = False
    print(camera.camera_flag)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    ip = get_ip.getIp()
    app.run(host=ip, port=8080, threaded=True)


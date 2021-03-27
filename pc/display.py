# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from PIL import Image, ImageDraw, ImageFont,ImageTk

# 这个必须在主线程，阻塞在最后
class Display:
    def __init__(self, camera, kInput, ping):
        self.camera = camera
        self.kInput = kInput
        self.ping = ping

        # 用于计算一个粗略的fps
        self.lastTime = 0.0
        self.lastFrameCount = 0
        self.fps = 0.0

    # 获取到了一帧的时候调用，用于计算粗略的帧速率，不准，但是可以接受
    def gotAFrame(self):
        if self.lastTime == 0.0:
            self.lastTime = time.time()

        self.lastFrameCount += 1

        now = time.time()
        #print(now - self.lastTime)
        if now - self.lastTime > 1:
            count = self.lastFrameCount
            t = now - self.lastTime
            self.fps = round(count / t)
            #print(self.fps)
            self.lastTime = now
            self.lastFrameCount = 0

        
    def start(self):
        while True:
            if self.camera:
                # add fps
                fps = 'fps:' + str(self.camera.fps)
                frame = cv2.putText(self.camera.frame,fps,
                (20, 30), fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0,0,0xff),
                thickness=1, lineType=cv2.LINE_AA)

                #add display fps
                self.gotAFrame()
                d_fps = 'display fps:' + str(self.fps)
                frame = cv2.putText(self.camera.frame, d_fps,
                (200, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0, 0, 0xff),
                thickness=1, lineType=cv2.LINE_AA)

                # ping
                pingDt = 'ping:' + str(self.ping.getDt()) + 'ms'
                frame = cv2.putText(self.camera.frame, pingDt,
                (500, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0, 0, 0xff),
                thickness=1, lineType=cv2.LINE_AA)



                # add kInput
                i = self.kInput.ctrl
                if i['up']==1 :
                    frame = cv2.putText(self.camera.frame,'U',
                    (540, 440),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.2, color=(0,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                else :
                    frame = cv2.putText(self.camera.frame,'U',
                    (540, 440),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0xff,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                if i['down']==1 :
                    frame = cv2.putText(self.camera.frame,'D',
                    (540, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.2, color=(0,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                else :
                    frame = cv2.putText(self.camera.frame,'D',
                    (540, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0xff,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                if i['left']==1 :
                    frame = cv2.putText(self.camera.frame,'L',
                    (510, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.2, color=(0,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                else :
                    frame = cv2.putText(self.camera.frame,'L',
                    (510, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0xff,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)

                if i['right']==1 :
                    frame = cv2.putText(self.camera.frame,'R',
                    (570, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.2, color=(0,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)
                else :
                    frame = cv2.putText(self.camera.frame,'R',
                    (570, 470),  fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0xff,0xff,0xff),
                    thickness=1, lineType=cv2.LINE_AA)





                cv2.imshow("cam", frame)
                if self.camera.fps != 0:
                    key = cv2.waitKey(round(900/self.camera.fps))
                else:
                    key = cv2.waitKey(1)




def addText2Image(self,image,text,color,font,siz,pos):
        # 图像从OpenCV格式转换成PIL格式
        img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # 字体  字体*.ttc的存放路径一般是： /usr/share/fonts/opentype/noto/ 查找指令locate *.ttc
        font = ImageFont.truetype(font, siz)
        # 字体颜色
        fillColor = color
        
        # 需要先把输出的中文字符转换成Unicode编码形式
        if not isinstance(text, str):
            text = text.decode('utf8')
    
        draw = ImageDraw.Draw(img_PIL)
        line_width, line_height = draw.textsize(text, font)
        (x,y)=pos
        position = (x-line_width/2,y-line_height/2)
        draw.text(position, text, font=font, fill=fillColor)
    
        # 转换回OpenCV格式
        image_new = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)
        return image_new



if __name__ == '__main__':
    # image = cv2.imread('1.png')
    # srcFilename = '驴鞭的功效与作用有哪些？.mp4'
    # # (h,w,_) = image.shape
    # # print(w,h)
    # red = (255,0,0)
    # font = 'STHeiti Medium.ttc'
    # # imageNew = addText2Image(image,'功效',red,font,30,(w/2,h/2))
    # # cv2.imwrite('02.jpg',imageNew)
    # # addText2mov(srcFilename,'aaa.mp4','lvbiandegongxiao\n   驴鞭的功效',red,font,70,(1280/2,720/2),0,5)
    # image = addText2movPreview(srcFilename,'lvbiandegongxiao\n         驴鞭的功效',red,font,70,(1280/2,720/2),0,5)
    # cv2.imwrite('02.jpg',image)
    # print('ok')
    display = Display('')
    frame = np.zeros(368*640*3,dtype="float32").reshape(368,640,3)
    frame = display.addText2Image(frame,'AAA','red','hei.ttf',30,(368/2,640/2))
    cv2.imwrite('02.jpg',frame)
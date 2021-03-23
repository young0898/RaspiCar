import cv2
import socket


def start_camera_service():
    #server_address = ('192.168.3.100', 12305)
    server_address = ('192.168.31.61', 12305)

    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   #socket对象
    server.connect(server_address)
    print('now starting to send frames...')

    camera = cv2.VideoCapture(0) #VideoCapture对象，可获取摄像头设备的数据
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH,960)
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    #camera.set(cv2.CAP_PROP_POS_FRAMES, 30)

    print('sent the frame')
    while camera.isOpened():
        success, frame = camera.read()
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  #编码
        try:
            server.sendall(imgencode) #发送视频帧数据
        except Exception as e:
            print(e)
            break

    camera.release()
    server.close()

if __name__ == '__main__':
    start_camera_service()
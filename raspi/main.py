import eventlet   # eventlet包提供了协程的支持
import socketio
from control_car import Control_Car
from control_function import Control_Function

sio = socketio.Server()    #1 创建socketio服务器
app = socketio.WSGIApp(sio)   #2 创建应用

carControl = Control_Car()   # 实例化车辆控制（舵机和电调）
functionControl = Control_Function()  # 实例化功能控制（开关灯、开关摄像头....）

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def init(sid, data):
    print('init ', data)
    carControl.initCarControl(data)

@sio.event
def ctrl(sid, data):
    print('ctrl ', data)
    carControl.set(data)

@sio.event
def ctrlRaw(sid, data):
    print('ctrlRaw ', data)
    carControl.setRaw(data)

@sio.event
def ping(sid, data):
    #print('ping', data)
    sio.emit('ping', data) #啥都不做，直接转发原data回去

@sio.event
def exec(sid, data):
    print('exec ', data)
    functionControl.execute(data['cmd'])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    socket = eventlet.listen(('', 12306))    #3 监听端口
    eventlet.wsgi.server(socket, app)      #4 启动服务器
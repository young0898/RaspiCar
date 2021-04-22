import eventlet   # eventlet包提供了协程的支持
import socketio
from control_car import Control_Car
from control_function import Control_Function
import get_ip

print('初始化socketio服务')
sio = socketio.Server(cors_allowed_origins="*")    #1 创建socketio服务器
app = socketio.WSGIApp(sio)   #2 创建应用

carControl = Control_Car()   # 实例化车辆控制（舵机和电调）
carControl.initCarControl()
functionControl = Control_Function()  # 实例化功能控制（开关灯、开关摄像头....）
#functionControl.initWebServer()  # 初始化web服务
functionControl.initFlask()   # 初始化Flask web服务

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    carControl.initCarControl()
    sio.emit('init', {'direction_add': carControl.direction_add,
                    'direction_per': carControl.direction_per,
                    'direction_reverse': carControl.direction_reverse,
                    'speed_add': carControl.speed_add,
                    'speed_per': carControl.speed_per})

@sio.event
def init(sid, data):
    print('init ', data)
    #carControl.initCarControl(data)

@sio.event
def ctrl(sid, data):
    print('ctrl ', data)
    carControl.ctrl(data)

@sio.event
def set(sid, data):
    print('set ', data)
    carControl.set(data)

@sio.event
def ping(sid, data):
    #print('ping', data)
    sio.emit('ping', data)

@sio.event
def exec(sid, data):
    print('exec ', data)
    functionControl.execute(data['cmd'])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    ip = get_ip.getIp()
    socket = eventlet.listen((ip, 12306))    #3 监听端口
    eventlet.wsgi.server(socket, app)      #4 启动服务器
    # eventlet是一个协程库, 其中提供了服务器代码, 而且该服务器支持websocket协议的

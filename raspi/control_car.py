import RPi.GPIO as GPIO
from config import global_config
import time

servo_pin = 12  # 定义舵机pwm输出引脚
motor_pin = 13  # 定义电调pwm输出引脚
frequency = 50  #定义pwm输出频率

class Control_Car:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # 定义树莓派GPIO引脚以BCM方式编号
        GPIO.setwarnings(False)
        GPIO.setup(servo_pin, GPIO.OUT)  # 设置舵机IO口为输出
        GPIO.setup(motor_pin, GPIO.OUT)  # 设置电调IO口为输出
        self.servo_pwm = GPIO.PWM(servo_pin, frequency)  # 定义舵机pwm输出频率
        self.motor_pwm = GPIO.PWM(motor_pin, frequency)  # 定义电调pwm输出频率
        self.direction_add = int(global_config.get('config', 'direction_add'))   # 左右方向修正
        self.direction_per = float(global_config.get('config', 'direction_per'))  # 最大转向角度占比
        self.direction_reverse = int(global_config.get('config', 'direction_reverse'))  # 方向反向
        self.speed_add = int(global_config.get('config', 'speed_add'))  # 前进后退修正
        self.speed_per = float(global_config.get('config', 'speed_per'))   # 速度比例100%

        self.last_direction = 0
        self.last_speed = 0

    def initCarControl(self):
        direction = 0
        speed = 0
        self.servo_duty = (direction * self.direction_per + self.direction_add) * self.direction_reverse / 90 * 5 + 7.5  # 占空比  -90度：0.5ms 2.5%； 0度：1.5ms 7.5%； 90度：2.5ms 12.5%
        self.motor_duty = (speed * self.speed_per + self.speed_add) / 100 * 2.5 + 7.5   # 占空比  1ms 5%,  1.5ms 7.5%   2ms 10%
        self.servo_pwm.start(self.servo_duty)
        self.motor_pwm.start(self.motor_duty)
        self.servo_pwm.ChangeDutyCycle(0)  # 清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止



    def carCtrl(self, speed, direction):
        if self.last_speed != speed:
            newSpeed = speed * self.speed_per + self.speed_add
            if newSpeed <= -100:
                newSpeed = -100
            elif newSpeed >= 100:
                newSpeed = 100
            self.motor_duty = newSpeed / 100 * 2.5 + 7.5
            self.motor_pwm.ChangeDutyCycle(self.motor_duty)
            self.last_speed = speed

        if self.last_direction != direction:
            newDirection = (direction * self.direction_per + self.direction_add) * self.direction_reverse
            if newDirection <= -90:
                newDirection = -90
            elif newDirection >= 90:
                newDirection = 90
            self.servo_duty = newDirection / 90 * 5 + 7.5
            self.servo_pwm.ChangeDutyCycle(self.servo_duty)
            self.last_direction = direction

        if direction == 0 and speed == 0:
            #print("delay and ChangeDutyCycle = 0")
            time.sleep(0.03)  # 等待控制周期结束
            self.servo_pwm.ChangeDutyCycle(0)  # 清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止






        # print("direction =", direction, "-> duty =", self.servo_duty, '%')
        #time.sleep(0.02)  # 等待控制周期结束
        #self.servo_pwm.ChangeDutyCycle(0)  # 清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止

    def setDirectionAdd(self, direction_add):
        self.direction_add = direction_add
        global_config.set('config', 'direction_add', str(self.direction_add))

    def setDirectionPer(self, direction_per):
        self.direction_per = direction_per
        global_config.set('config', 'direction_per', str(self.direction_per))

    def setDirectionReverse(self, direction_reverse):
        self.direction_reverse = direction_reverse
        global_config.set('config', 'direction_reverse', str(self.direction_reverse))

    def setSpeedAdd(self, speed_add):
        self.speed_add = speed_add
        global_config.set('config', 'speed_add', str(self.speed_add))

    def setSpeedPer(self, speed_per):
        self.speed_per = speed_per
        global_config.set('config', 'speed_per', str(self.speed_per))




    def ctrl(self, data):
        if 'speed' in data and 'direction' in data:
            self.carCtrl(data['speed'], data['direction'])

    def set(self, data):
        if 'direction_add' in data:
            self.setDirectionAdd(data['direction_add'])
        if 'direction_per' in data:
            self.setDirectionPer(data['direction_per'])
        if 'direction_reverse' in data:
            self.setDirectionReverse(data['direction_reverse'])
        if 'speed_add' in data:
            self.setSpeedAdd(data['speed_add'])
        if 'speed_per' in data:
            self.setSpeedPer(data['speed_per'])
        self.initCarControl()

    def carClose(self):
        #self.initCarControl()
        #self.motor_pwm.stop()
        #self.servo_pwm.stop()
        GPIO.cleanup()

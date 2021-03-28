import RPi.GPIO as GPIO

servo_pin = 12  # 定义舵机pwm输出引脚
motor_pin = 13  # 定义电调pwm输出引脚
frequency = 50  #定义pwm输出频率

class Control_Car:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # 定义树莓派GPIO引脚以BCM方式编号
        GPIO.setup(servo_pin, GPIO.OUT)  # 设置舵机IO口为输出
        GPIO.setup(motor_pin, GPIO.OUT)  # 设置电调IO口为输出
        self.servo_pwm = GPIO.PWM(servo_pin, frequency)  # 定义舵机pwm输出频率
        self.motor_pwm = GPIO.PWM(motor_pin, frequency)  # 定义电调pwm输出频率

    def initCarControl(self, direction):
        self.servo_duty = 90 / 180 * 5 + 5  # 占空比  0度：0.5ms 2.5%； 90度：1.5ms 7.5%； 180度：2.5ms 12.5%
        self.motor_duty = 112 / 254 * 5 + 5   # 占空比  1ms 5%,  1.5ms 7.5%   2ms 10%
        self.servo_pwm.start(self.servo_duty)
        self.motor_pwm.start(self.motor_duty)

    def setDirection(self, direction):
        new_diretion = 90
        if direction <= 10:
            new_diretion = 10
        elif direction >= 170:
            new_diretion = 170
        else:
            new_diretion = direction
        self.servo_duty = new_diretion / 180 * 10 + 2.5
        self.servo_pwm.ChangeDutyCycle(self.servo_duty)
        #print("direction =", new_diretion, "-> duty =", self.duty, '%')
        #time.sleep(0.01)

    def setSpeed(self, speed):
        self.motor_duty = speed / 254 * 5 + 5
        self.motor_pwm.ChangeDutyCycle(self.motor_duty)
        print("speed =", speed)
        #time.sleep(0.01)

    def set(self, data):
        if 'direction' in data:
            self.setDirection(data['direction'])
        if 'speed' in data:
            self.setSpeed(data['speed'])

    def setRaw(self, data):
        if 'direction' in data:
            self.setDirection(data['direction'])
        if 'speed' in data:
            self.setSpeed(data['speed'])
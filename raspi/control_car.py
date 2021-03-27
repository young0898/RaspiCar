import RPi.GPIO as GPIO

Servo_pin = 12  # 定义舵机pwm输出引脚
Servo_frequency = 50  #定义舵机pwm输出频率

class Control_Car:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # 定义树莓派GPIO引脚以BCM方式编号
        GPIO.setup(Servo_pin, GPIO.OUT)  # 使能GPIO口为输出
        self.pwm = GPIO.PWM(Servo_pin, Servo_frequency)  # 定义pwm输出频率
        self.duty = 90 / 180 * 10 + 2.5  # 占空比  0度：2.5%，90度：7.5%，180度：12.5%
        self.pwm.start(self.duty)

    def setDirection(self, direction):
        new_diretion = 90
        if direction <= 10:
            new_diretion = 10
        elif direction >= 170:
            new_diretion = 170
        else:
            new_diretion = direction
        self.duty = new_diretion / 180 * 10 + 2.5
        self.pwm.ChangeDutyCycle(self.duty)
        #print("direction =", new_diretion, "-> duty =", self.duty, '%')
        #time.sleep(0.01)

    def set(self, data):
        if 'direction' in data:
            self.setDirection(data['direction'])

    def setRaw(self, data):
        if 'direction' in data:
            self.setDirection(data['direction'])
    
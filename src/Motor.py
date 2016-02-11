import RPi.GPIO as GPIO
import time

class Motor:
	def __init__(self):
                self.init_gpio()
                
	def init_gpio(self):
                GPIO.setmode(GPIO.BCM)
	    
                channel_list = [14, 15, 18]
                GPIO.setup(channel_list, GPIO.OUT)

	def stop(self):
                GPIO.output(14, False)
                GPIO.output(15, False)
                GPIO.output(18, False)

	def rotate_right(self, duration):
		self.stop()
		GPIO.output(14, True)
		GPIO.output(15, False)
		GPIO.output(18, True)
		time.sleep(duration)
		self.stop()

	def rotate_left(self, duration):
                self.stop()
                GPIO.output(14, False)
                GPIO.output(15, True)
                GPIO.output(18, True)
                time.sleep(duration)
                self.stop()

	def cleanup(self):
                GPIO.cleanup()

if __name__ == "__main__":
	motor = Motor()

        motor.init_gpio()
	motor.rotate_right(2)
	motor.rotate_left(2)
	motor.cleanup()

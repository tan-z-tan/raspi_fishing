import RPi.GPIO as GPIO
import time

# Use pin number mode
GPIO.setmode(GPIO.BCM)

channel_list = [14, 15, 18]
GPIO.setup(channel_list, GPIO.OUT)

GPIO.output(14, True)
GPIO.output(15, True)
GPIO.output(18, True)

time.sleep(2)

GPIO.output(18, False)

GPIO.cleanup()
import RPi.GPIO as GPIO
import time

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    
    channel_list = [14, 15, 18]
    GPIO.setup(channel_list, GPIO.OUT)

def stop():
    GPIO.output(14, False)
    GPIO.output(15, False)
    GPIO.output(18, False)

def rotate_right(duration):
    stop()
    GPIO.output(14, True)
    GPIO.output(15, False)
    GPIO.output(18, True)
    time.sleep(duration)
    stop()

def rotate_left(duration):
    stop()
    GPIO.output(14, False)
    GPIO.output(15, True)
    GPIO.output(18, True)
    time.sleep(duration)
    stop()

def cleanup():
    GPIO.cleanup()


init_gpio()

rotate_right(2)

rotate_left(2)

cleanup()

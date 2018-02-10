#! /usr/bin/env python

import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def move_callback(channel):
    if GPIO.input(27):
        print('Movement')
        GPIO.output(17, GPIO.HIGH)
        sleep(2)
        GPIO.output(17, GPIO.LOW)

print('Starting movement tracking for 120 seconds')

GPIO.add_event_detect(27, GPIO.RISING, callback=move_callback, bouncetime=300)

try:
    sleep(120)
finally:
    GPIO.cleanup()

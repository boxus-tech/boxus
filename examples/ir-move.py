#! /usr/bin/env python

import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
# GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN)

def move_callback(channel):
    sleep(0.5)

    if GPIO.input(27):
        print('Movement')
        GPIO.output(17, GPIO.HIGH)
        sleep(2)
        GPIO.output(17, GPIO.LOW)

        # GPIO.remove_event_detect(27)
        # sleep(5)
        # GPIO.add_event_detect(27, GPIO.RISING, callback=move_callback, bouncetime=300)

# GPIO.add_event_detect(27, GPIO.RISING, callback=move_callback, bouncetime=300)

try:
    sleep(30)
finally:
    GPIO.cleanup()

while True:
    if GPIO.input(27):
        print('Movement')
        GPIO.output(17, GPIO.HIGH)
        sleep(2)
        GPIO.output(17, GPIO.LOW)

    else:
        print('No movement')
        sleep(0.5)

#! /usr/bin/env python

import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

while True:
    if GPIO.input(27):
        print('Movement')
        GPIO.output(17, GPIO.HIGH)
        sleep(2)
        GPIO.output(17, GPIO.LOW)

    else:
        print('No movement')
        sleep(0.5)

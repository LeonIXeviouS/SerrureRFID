#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, g, session, url_for, redirect, flash
import hashlib
import requests
import schedule
import time
import datetime
import RPi.GPIO as GPIO
from pirc522 import RFID

#from serrure import turn_high, turn_low, open_door

LED_GREEN = 5
LED_RED = 7
SERVO = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def init():
    GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SERVO, GPIO.OUT, initial=GPIO.LOW)

def setAngle(angle):
    pwm=GPIO.PWM(SERVO, 50)
    duty = angle / 18 + 2
    GPIO.output(SERVO, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

def turn_high (gpio) :
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)

def turn_low (gpio) :
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)

def open_door():
    pwm=GPIO.PWM(SERVO, 50)
    pwm.start(0)
    setAngle(180)
    time.sleep(3)
    setAngle(0)
    time.sleep(1)
    pwm.stop()
#Construct app
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('secret_config')
init()

#Pages
@app.route('/')
def index () :
    return render_template('index.html')

@app.route('/logs')
def showLogs():
    with open('/home/pi/log.txt') as event_log:
        event_lines = event_log.readlines()

        door_history = []
        events = len(event_lines)

        for x in range(events):
            door_history.append(event_lines[x].split(" "))

    return render_template('door-logs.html', events=events, door_history=door_history)

@app.route('/open-door/')
def openDoor():
    pwm=GPIO.PWM(SERVO, 50)
    turn_high(LED_GREEN)
    flash('The door is opened !')
    open_door()
    turn_low(LED_GREEN)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.100')

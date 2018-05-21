#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-

import time, re, os
from pirc522 import RFID
import RPi.GPIO as GPIO

LED_RED = 7
LED_GREEN = 5
SERVO = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def init():
    GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SERVO, GPIO.OUT, initial=GPIO.LOW)

def turn_high (gpio) :
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)

def turn_low (gpio) :
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)

def scan_badge():
    print("En attente de badge...")
    rc522.wait_for_tag()
    print("Badge detecté")

def add_log(ID, door):
    os.chdir('/home/pi/')
    fichier = open("log.txt", "a")
    fichier.write('----------------------\n')
    fichier.write('Badge : '+ID+'\n')
    if door:
        fichier.write('Badge Autorisé\n')
    else:
        fichier.write('Badge Refusé\n')
    fichier.write(time.strftime("%A %d %B %Y %H:%M:%S")+"\n")
    fichier.write('----------------------\n')
    fichier.close()
    print('>> Log ajouté')



def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

def open_door():
    pwm.start(0)
    setAngle(180)
    time.sleep(3)
    setAngle(0)
    time.sleep(1)
    pwm.stop()

def setDown():
    turn_low(LED_RED)
    turn_low(LED_GREEN)

init()

rc522 = RFID()
cardAuto = [
'[6715944131115]',
'[11511121729216]',
'[23413518099186]'
]



while True :

    scan_badge()

    (error, tag_type) = rc522.request()

    if not error :
        (error, uid) = rc522.anticoll()

        if not error :
            print('UID : {}'.format(uid))
            card = format(uid)
            cardnow = str(re.sub('[, ]', '', card))
            i = 0
            z = 0
            for c in cardAuto:
                i += 1 
                if cardnow == c:
                    add_log(cardnow, True)
                    print("Badge Autorisé")
                    pwm=GPIO.PWM(SERVO, 50)
                    turn_high(LED_GREEN)
                    open_door()
                    turn_low(LED_GREEN)
                elif i == len(cardAuto) and cardnow != c:
                    add_log(cardnow, False)
                    print("Bad Refusé")
                    turn_high(LED_RED)
                    time.sleep(3)
                    turn_low(LED_RED)
    setDown()

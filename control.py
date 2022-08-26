#!/usr/bin/env python3
import serial
import time
import RPi.GPIO as GPIO

mot_1_1 = 4
mot_1_2 = 17
mot_2_1 = 27
mot_2_2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup([mot_1_1, mot_1_2, mot_2_1, mot_2_2], GPIO.OUT)

def forward():
    print("going forward")
    GPIO.output(mot_1_1, GPIO.HIGH)
    GPIO.output(mot_1_2, GPIO.LOW)
    GPIO.output(mot_2_1, GPIO.LOW)
    GPIO.output(mot_2_2, GPIO.HIGH)
    return

def rotate1():
    print("rotating 1")
    GPIO.output(mot_1_1, GPIO.HIGH)
    GPIO.output(mot_1_2, GPIO.LOW)
    GPIO.output(mot_2_1, GPIO.HIGH)
    GPIO.output(mot_2_2, GPIO.LOW)

def rotate2():
    print("rotating 1")
    GPIO.output(mot_1_1, GPIO.LOW)
    GPIO.output(mot_1_2, GPIO.HIGH)
    GPIO.output(mot_2_1, GPIO.LOW)
    GPIO.output(mot_2_2, GPIO.HIGH)

def backward():
    print("moving backward")
    GPIO.output(mot_1_1, GPIO.LOW)
    GPIO.output(mot_1_2, GPIO.HIGH)
    GPIO.output(mot_2_1, GPIO.HIGH)
    GPIO.output(mot_2_2, GPIO.LOW)

def stop():
    print("moving backward")
    GPIO.output(mot_1_1, GPIO.LOW)
    GPIO.output(mot_1_2, GPIO.LOW)
    GPIO.output(mot_2_1, GPIO.LOW)
    GPIO.output(mot_2_2, GPIO.LOW)


def cleanup():
    GPIO.cleanup()





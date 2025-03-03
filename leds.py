#!/usr/bin/env python3
"""Ultra simple sample on how to use the library"""
from apa102_pi.driver import apa102
import time
import RPi.GPIO  as GPIO

def start_leds(power_pin):
    power_pin = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_pin,GPIO.OUT)
    GPIO.output(power_pin,GPIO.HIGH)
    strip = apa102.APA102(num_led=12)
    return strip

def light(strip,angle):
    strip.clear_strip()
    led_nr=(round((angle/30)))
    strip.set_pixel_rgb(led_nr, 0x00FF00)  # Green
    strip.show()

def stop_leds(strip,power_pin):
    strip.clear_strip()
    strip.cleanup()
    GPIO.output(power_pin,GPIO.LOW)


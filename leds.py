#!/usr/bin/env python3
"""Ultra simple sample on how to use the library"""
from apa102_pi.driver import apa102
import time
import RPi.GPIO  as GPIO


def main():
    # Initialize power pin
    power_pin = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_pin,GPIO.OUT)
    GPIO.output(power_pin,GPIO.HIGH)

    # Initialize the library and the strip. This defaults to SPI bus 0, order 'rgb' and a very low brightness
    strip = apa102.APA102(num_led=12)

    # Turn off all pixels (sometimes a few light up when the strip gets power)
    strip.clear_strip()

    # Prepare a few individual pixels
    strip.set_pixel_rgb(1, 0xFF0000)  # Red
    strip.set_pixel_rgb(2, 0x0000FF)  # Blue
    strip.set_pixel_rgb(3, 0x00FF00)  # Green

    # Copy the buffer to the Strip (i.e. show the prepared pixels)
    strip.show()

    # Wait a few Seconds, to check the result
    time.sleep(5)

    # Clear the strip and shut down
    strip.clear_strip()
    strip.cleanup()

    # Turn off power pin 
    GPIO.output(power_pin,GPIO.LOW)

if __name__ == '__main__':
    main()

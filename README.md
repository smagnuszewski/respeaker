# 6mic array scripts

This readme describes usage of my custom scripts developed to work with seedstudio 6 mic rpi array.

## Installation
* [requirements.txt](./requirements.txt) via pip. 
* system libraries

```bash
sudo apt install python3-pyaudio
```


## leds.py

Example communication with leds via [apa102-pi library](https://github.com/tinue/apa102-pi) that is a port of apa102 to rpi platform. Leds on the board are connected in serial topology and are controlled via SPI (remember to enable SPI bus on Rpi ). 

GPIO5 is LED enable pin so must be `HIGH` when controlling LEDS.

### TODO

* Create a function that turns on selected LED.
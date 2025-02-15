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

## ODAS

Odas project enables DOA (direction of arrival) for rpi client.

### Installation
---
#### Install [odas](https://github.com/smagnuszewski/respeaker-odas) on rpi 

As the project is not maintained actively many dependencies heave to be installed in a uncommon fashion.

Add the following indexes to apt source list:
```
deb http://archive.raspberrypi.org/debian/ bullseye main
deb http://deb.debian.org/debian/ bullseye main contrib non-free
```
install apt dependencies:
```
sudo apt install libfftw3-dev libconfig-dev libasound2-dev libpulse-dev
```
Clone the repo:
```
git clone https://github.com/smagnuszewski/respeaker-odas
```
build the project:
```
cd respeaker-odas
mkdir build
cd build
cmake ../
make
```
---
#### Install [odas-web](https://github.com/smagnuszewski/respeaker-odas_web) on a server machine

Server requires `python2.7` and `node12`. As these are EOF please use the environment managers to avoid conflicts with system packages:

* Install `node 12`
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 12
nvm use 12
```
* Install `python2.7`:
```
curl -fsSL https://pyenv.run | bash
pyenv install 2.7.18
pyenv local 2.7.18
```

Configure npm to use `python2.7` and clean cache before installing `odas-server`:
```
git clone https://github.com/smagnuszewski/respeaker-odas_web
cd respeaker-odas_web
npm config set python python2.7
npm cache clean --force  
rm -rf node_modules package-lock.json
npm i
```

### Usage

At first start the server on the local machine:
```
cd respeaker-odas_web
npm start
```
Than start the odas app on rpi
```
./odas/build/bin/odaslive -c CONFIG
```

### Config

Corrected config that works is [custom.cfg](./custom.cfg)

In order to obtain the `card` and `device` fields of the `raw:interface`:
```
python get_index.py
```
Add the server ip to the `sst:interface`. It shows up in odas_web GUI.

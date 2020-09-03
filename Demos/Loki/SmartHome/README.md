# Requirements

- Raspberry Pi 4 Model B
- LED (2 Pin)
- [TFT LCD 2.4inch](https://github.com/adafruit/Adafruit_Python_ILI9341)
- [1602 LCD I2C](https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display)

---

# Raspberry Pi 4 Model B

### Raspberry Pi OS

[Download Raspbian Buster 2019-09-30](https://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/2019-09-26-raspbian-buster.zip)

```
Release Date: 2019-09-30
Release Name: 2019-09-26
```

### HDMI Setting

```
config.txt
hdmi_group=2
hdmi_mode=16
hdmi_driver=2
```

---

# Python 3.6.8

Install packages

```
$ sudo apt-get update
$ sudo apt-get install build-essential bzip2 libbz2-dev libreadline6 libreadline6-dev libffi-dev libssl1.0-dev sqlite3 libsqlite3-dev libjpeg-dev zlib1g-dev python3-rpi.gpio
```

Dwonload pyenv

```
$ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

Append to ~/.bashrc

```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Download python 3.6.8

```
$ source ~/.bashrc
$ pyenv install 3.6.8
$ pyenv virtualenv 3.6.8 SmartHome_3.6.8
$ cd ~/Desktop/SmartHome_3
$ pyenv local SmartHome_3.6.8
```

---

# Devices

### Connected Pin

```
RPi            1602 LCD with I2C
Pin 03  <--->  SDA
Pin 04  <--->  VCC
Pin 05  <--->  SCL
Pin 06  <--->  GND

RPi            TFT LCD with ILI9341 SPI
Pin 17  <--->  VCC
Pin 18  <--->  RST
Pin 19  <--->  MOSI
Pin 20  <--->  GND
Pin 22  <--->  DC
Pin 23  <--->  CLK

RPi            LED
Pin 35  <--->  LED 2
Pin 36  <--->  LED 1
Pin 37  <--->  LED 5
Pin 38  <--->  LED 3
Pin 39  <--->  LED 4
Pin 40  <--->  GND
```

### LED (light.py)

```
$ pip install gpiozero
$ pip install RPi.GPIO
```

### 1602 LCD with I2C (tv.py)

```
$ pip install Pillow
$ pip install RPLCD
$ pip install smbus2
```

### TFT LCD with ILI9341 SPI (ac.py)

```
$ wget https://github.com/adafruit/Adafruit_Python_ILI9341/archive/master.zip
$ unzip master.zip
$ cd Adafruit_Python_ILI9341-master
$ python setup.py install
$ pip install Pillow
$ pip install numpy
$ pip install Adafruit_GPIO
```

---

# Run

Open AIoT/AIoT.py

```
Line 37: USERNAME = "YOUR_ACCOUNT"
Line 38: LOKI_KEY = "YOUR_LOKI_KEY"
```

Open AIoT/intent/*.py

```
USERNAME = "YOUR_ACCOUNT"
API_KEY  = "YOUR_ARTICUT_KEY"
```

Launch server

```
$ pip install flask
$ pip install requests
$ python app.py
```

Access [http://localhost:5000/](http://localhost:5000/)
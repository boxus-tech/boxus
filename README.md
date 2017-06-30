Boxus
=====

[![PyPI version](https://badge.fury.io/py/boxus.svg)](https://badge.fury.io/py/boxus)
[![Travis-ci Status](https://travis-ci.org/boxus-plants/boxus.svg?branch=master)](https://travis-ci.org/boxus-plants/boxus)
[![Code Climate](https://codeclimate.com/github/boxus-plants/boxus/badges/gpa.svg)](https://codeclimate.com/github/boxus-plants/boxus)
[![Issue Count](https://codeclimate.com/github/boxus-plants/boxus/badges/issue_count.svg)](https://codeclimate.com/github/boxus-plants/boxus/issues)
[![Test Coverage](https://codeclimate.com/github/boxus-plants/boxus/badges/coverage.svg)](https://codeclimate.com/github/boxus-plants/boxus/coverage)

## About
Inspired by Ruby on Rails ActiveRecord and powered by [Nanpy](https://github.com/nanpy/) high-level framework for easy control of multiple devices connected to the Raspberry Pi and Arduino via GPIO. Core of the open DIY project of building automated plants grow pod.

Currently supported out of the box sensors:
* DHT digital temperature and humidity sensor (DHT11 tested)
* Analog soil moisture sensor (1. turn on power; 2. read analog input; 3. turn off power in order to minimize galvanic corrosion)
* Generic (digital and analog reads from one input pin)

and devices:
* Relay (turned on – `LOW` output state; turned off – default and `HIGH` output states)
* Generic (turned on – `HIGH` output state; turned off – default and `LOW` output states)

Use declarative YAML syntax to specify how your sensors and devices are connected, e.g.:
```yaml
sensors:
  -
    _id: sensor_1
    description: DHT11 Temperature and humidity sensor
    type_name: dht
    control: native
    measurements:
      - temperature
      - humidity
    pins:
      input:
        type: digital
        number: 4
        dht_version: 11

devices:
  -
    _id: dev_1
    description: Main water pump
    type_name: relay
    control: arduino
    arduino_port: /dev/ttyUSB0
    pins:
      power:
        type: digital
        number: 4
```

Put all seed info into the `yml` file (see e.g. [seed.example.yml](examples/db/seed.example.yml)) and use `DB` class to import it into the `CouchDB`:
```python
from boxus import DB

db = DB()
db.seed('/path/to/seed.yml')
```

Then easily read all your sensors and save data into the `CouchDB`
```python
from boxus import DB, Sensor

db = DB()

sensors = Sensor.all(db)

for s in sensors:
    s.read()
```
turn on/off your devices
```python
from boxus import DB, Device

db = DB()

dev = Device.find(db, 'dev_1')
dev.on()
dev.off()
```
or create a watchdog script (see [watchdog.py example](examples/watchdog.py)) and install CRON job using `Manager`:
```python
from boxus import Manager

manager = Manager()
# E.g. every 10 minutes
manager.install_cron('/path/to/python /path/to/watchdog.py', 10)
```

## Installation

### Requirements

MacOS
```shell
brew install couchdb
```
or Linux
```shell
sudo apt-get install couchdb
```

### The latest development build

```shell
git clone https://github.com/boxus-plants/boxus.git
cd boxus
pip install -e .
```

### The latest stable release

```shell
pip install boxus
```

## Requirements

### Hardware

* Raspberry Pi (Pi 3 tested)
* Arduino (Nano v3 tested)

### Software

#### Required
* [CouchDB](http://couchdb.apache.org)

#### Optional
* [Nanpy Firmware for Arduino](https://github.com/nanpy/nanpy-firmware) for easy Arduino control and analog sensors support
* [Adafruit Python DHT library](https://github.com/adafruit/Adafruit_Python_DHT) for reading temperature and humidity data from DHT sesnors connected directly to Raspberry Pi

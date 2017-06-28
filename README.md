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
* Analog soil moisture sensor

Use declarative YAML syntax to specify how your sensors and devices are connected, e.g.:
```yaml
sensors:
  -
    _id: sensor_1
    description: DHT11 Temperature and humidity sensor
    sensor_type: dht
    control: native
    measurements:
      - temperature
      - humidity
    pins:
      input:
        type: digital
        number: 4
        dht_version: 11
  -
    _id: sensor_2
    description: Moisture sensor
    sensor_type: moisture
    control: arduino
    arduino_port: /dev/ttyUSB0
    measurements:
      - moisture
    pins:
      power:
        type: digital
        number: 5
      input:
        type: analog
        number: 15
```

Put all seed info into the `yml` file (see e.g. [seed.example.yml](examples/db/seed.example.yml)) and use `Manager` class to import it into the `CouchDB`:
```python
from boxus import DB, Manager

db = DB()

manager = Manager(db)
manager.seed('/path/to/seed.yml')
```

Then easily read your sensors and save data into the `CouchDB`
```python
from boxus import DB, Sensor

db = DB()

sensors = Sensor.all(db.sensors)

for s in sensors:
    s.read()
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

import warnings
import time
import csv

# Platform-specific modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    warnings.warn('Please, install RPi.GPIO library', Warning)
try:
    import Adafruit_DHT as DHT
except ImportError:
    warnings.warn('Please, install Adafruit_DHT from https://github.com/adafruit/Adafruit_Python_DHT in order to use DHT sensors.', Warning)

from couchdb.mapping import TextField, ListField, DateTimeField
from datetime        import datetime, timedelta

from .controllable  import Controllable
from .reading       import Reading
from .utils         import *

class Sensor(Controllable):
    measurements    = ListField(TextField())

    supported_types = [
        'generic',
        'dht',
        'moisture'
    ]

    db_name = 'sensors'

    def readings_iter(self, options=dict()):
        return self.db.readings.query('''
                function(doc) {
                    if(doc.sensor_id && doc.sensor_id == '%s'){
                        emit(doc.created_at, doc);
                    }
                }
            ''' % self.id, None, 'javascript', Reading._wrapper, **options)

    def readings(self, options=dict()):
        return list(self.readings_iter(options))

    def readings_for(self, n, units='days', options=dict()):
        seconds = human_interval_to_seconds(n, units)
        field = DateTimeField()
        options['startkey'] = field._to_json(datetime.today() - timedelta(seconds=seconds))

        return self.readings(options)

    def readings_to_csv(self, path):
        with open(path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for r in self.readings_iter():
                writer.writerow(map(str, r.values) + [r.created_at])

    def save_readings(self, values):
        r = Reading(self.db)
        r.sensor_id = self.id
        r.values = values
        r.save()

        return True

    def read(self):
        return self._send_control_sequence('read', self.type_name)

    def _read_generic(self):
        value = None

        if self.control == 'native':
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pins['input']['number'], GPIO.IN)

            value = GPIO.input(self.pins['input']['number'])

        elif self.control == 'arduino':
            with self.arduino_api_scope() as api:
                api.pinMode(self.pins['input']['number'], api.INPUT)

                if self.pins['input']['type'] == 'analog':
                    value = api.analogRead(self.pins['input']['number'])
                elif self.pins['input']['type'] == 'digital':
                    value = api.digitalRead(self.pins['input']['number'])

        if value is not None:
            self.save_readings([value])

        return value

    def _read_dht(self):
        humidity, temperature = DHT.read_retry(
                self.pins['input']['dht_version'],
                self.pins['input']['number']
            )

        self.save_readings([temperature, humidity])

        return temperature, humidity

    def _read_moisture(self):
        moisture = None

        with self.arduino_api_scope() as api:
            api.pinMode(self.pins['input']['number'], api.INPUT)
            api.pinMode(self.pins['power']['number'], api.OUTPUT)

            # Turn on moisture sensor power
            api.digitalWrite(self.pins['power']['number'], api.HIGH)

            # Wait a few seconds to stabilize readings
            time.sleep(3)
            moisture = api.analogRead(self.pins['input']['number'])

            # Turn off moisture sensor power
            api.digitalWrite(self.pins['power']['number'], api.LOW)

        self.save_readings([moisture])

        return moisture

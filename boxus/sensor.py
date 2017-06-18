import warnings
import time

try:
    import Adafruit_DHT as DHT
except ImportError:
    warnings.warn('Please, install Adafruit_DHT from https://github.com/adafruit/Adafruit_Python_DHT in order to use DHT sensors.', Warning)

from couchdb.mapping import TextField, ListField, DictField

from nanpy import SerialManager
from nanpy import ArduinoApi

from .document_base import DocumentBase
from .db            import DB

from .reading import Reading

class Sensor(DocumentBase):
    description     = TextField()
    sensor_type     = TextField()
    control         = TextField()
    measurements    = ListField(TextField())
    pins            = DictField()

    def read(self):
        if self.sensor_type == 'dht':
            return self.read_dht()
        elif self.sensor_type == 'moisture':
            return self.read_moisture()
        else:
            warnings.warn('Readings for this sensor type (%s) are not yet implemented' % self.sensor_type, FutureWarning)
            return None

    def read_dht(self):
        db = DB()
        db.connect()

        humidity, temperature = DHT.read_retry(
            self.pins['input']['dht_version'], 
            self.pins['input']['number'])

        r = Reading(db.readings)
        r.sensor_id = self.id
        r.values = [temperature, humidity]
        r.save()

        return temperature, humidity

    def read_moisture(self):
        db = DB()
        db.connect()

        connection = SerialManager(device='/dev/ttyUSB0')
        arduino = ArduinoApi(connection=connection)

        arduino.pinMode(self.pins['input']['number'], arduino.INPUT)
        arduino.pinMode(self.pins['power']['number'], arduino.OUTPUT)

        # Turn on moisture sensor power
        arduino.digitalWrite(self.pins['power']['number'], arduino.HIGH)

        # Wait 5 seconds to stabilize readings
        time.sleep(5)
        moisture = arduino.analogRead(self.pins['input']['number'])

        # Turn off moisture sensor power
        arduino.digitalWrite(self.pins['power']['number'], arduino.LOW)

        connection.close()

        r = Reading(db.readings)
        r.sensor_id = self.id
        r.values = [moisture]
        r.save()

        return moisture

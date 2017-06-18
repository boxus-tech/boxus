import warnings

from couchdb.mapping import TextField, ListField, DictField

from .document_base import DocumentBase
from .db            import DB

class Sensor(DocumentBase):
    sensor_type     = TextField()
    control         = TextField()
    measurements    = ListField(TextField())
    pins            = DictField()

    def read(self):
        db = DB()
        db.connect()

        if self.sensor_type == 'dht':
            return self.read_dht()
        elif self.sensor_type == 'moisture':
            return self.read_moisture()
        else:
            warnings.warn('Readings for this sensor type (%s) are not yet implemented' % self.sensor_type, FutureWarning)
            return None

    def read_dht(self):
        return None

    def read_moisture(self):
        return None

from datetime import datetime

from couchdb.mapping import Document, TextField, DateTimeField, ListField, DictField

class Sensor(Document):
    description     = TextField()
    created_at      = DateTimeField()
    updated_at      = DateTimeField()
    sensor_type     = TextField()
    control         = TextField()
    measurements    = ListField(TextField())
    pins            = DictField()

    def save(self, db):
        if not self.created_at:
            self.created_at = datetime.now()
        else:
            self.updated_at = datetime.now()

        self.store(db)

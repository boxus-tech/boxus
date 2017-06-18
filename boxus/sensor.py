from couchdb.mapping import Document, TextField, ListField, DictField

from .document_base import DocumentBase

class Sensor(DocumentBase):
    sensor_type     = TextField()
    control         = TextField()
    measurements    = ListField(TextField())
    pins            = DictField()

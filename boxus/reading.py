from couchdb.mapping import TextField, ListField, FloatField

from .document_base import DocumentBase

class Reading(DocumentBase):
    sensor_id   = TextField()
    values      = ListField(FloatField())

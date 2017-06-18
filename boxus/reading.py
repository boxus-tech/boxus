from couchdb.mapping import TextField, DictField

from .document_base import DocumentBase

class Reading(DocumentBase):
    sensor_id   = TextField()
    values      = DictField()

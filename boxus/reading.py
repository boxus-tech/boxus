from couchdb.mapping import TextField, ListField, FloatField

from .dbase import DBase

class Reading(DocumentBase):
    __tablename__ = 'readings'
    
    sensor_id   = TextField()
    values      = ListField(FloatField())

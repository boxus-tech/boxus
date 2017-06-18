from couchdb.mapping import TextField, DictField

from .document_base import DocumentBase

class Device(DocumentBase):
    description     = TextField()
    control         = TextField()
    pins            = DictField()

from couchdb.mapping import TextField, DictField

from .document_base import DocumentBase

class Device(DocumentBase):
    control         = TextField()
    pins            = DictField()

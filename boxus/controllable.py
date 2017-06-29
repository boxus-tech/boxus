import warnings
from contextlib import contextmanager

from couchdb.mapping import TextField, DictField
from nanpy import SerialManager
from nanpy import ArduinoApi

from .document_base import DocumentBase

class Controllable(DocumentBase):
    type_name       = TextField()
    control         = TextField()
    pins            = DictField()
    arduino_port    = TextField()

    supported_control_types = [
        'native',
        'arduino'
    ]

    supported_types = []

    def check_type(self):
        if self.type_name in self.supported_types:
            return True
        else:
            warnings.warn('Control of "%s" type are not yet implemented' % self.type_name, FutureWarning)
            return False

    def check_control(self):
        if self.control in self.supported_control_types:
            return True
        else:
            warnings.warn('Devices and sensors should be connected directly to Raspberry Pi or via slave Arduino', Warning)
            return False

    @contextmanager
    def arduino_api_scope(self):
        connection = SerialManager(device=self.arduino_port)
        arduino = ArduinoApi(connection=connection)

        try:
            yield arduino
        finally:
            connection.close()

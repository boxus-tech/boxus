import warnings
from contextlib import contextmanager

from couchdb.mapping import TextField, DictField, BooleanField
from nanpy import SerialManager
from nanpy import ArduinoApi

from .document_base import DocumentBase

class Controllable(DocumentBase):
    type_name       = TextField(default='generic')
    control         = TextField()
    pins            = DictField()
    arduino_port    = TextField()
    deactivated     = BooleanField()
    description     = TextField()

    supported_control_types = [
        'native',
        'arduino'
    ]

    supported_types = []

    @contextmanager
    def arduino_api_scope(self):
        connection = SerialManager(device=self.arduino_port)
        arduino = ArduinoApi(connection=connection)

        try:
            yield arduino
        finally:
            connection.close()

    def _check_status(self):
        if not self.deactivated:
            return True
        else:
            warnings.warn('Controlable device "%s" is deactivated' % self.description, Warning)
            return False

    def _check_type(self):
        if self.type_name in self.supported_types:
            return True
        else:
            warnings.warn('Control of "%s" type are not yet implemented' % self.type_name, FutureWarning)
            return False

    def _check_control(self):
        if self.control in self.supported_control_types:
            return True
        else:
            warnings.warn('''
                Devices and sensors should be connected directly
                to Raspberry Pi (control="native") or
                via slave Arduino (control="arduino")''', Warning)
            return False

    def _send_control_sequence(self, prefix, postfix, return_on_fail=None):
        if self._check_status() and \
           self._check_type() and \
           self._check_control():
            return getattr(self, '_%s_%s' % (prefix, postfix))()
        else:
            return return_on_fail

    def _digital_out(self, pin, val):
        if self.control == 'native':
            value = GPIO.HIGH if val == 1 else GPIO.LOW

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, value)

        elif self.control == 'arduino':
            with self.arduino_api_scope() as api:
                value = api.HIGH if val == 1 else api.LOW

                api.pinMode(pin, api.OUTPUT)
                api.digitalWrite(pin, value)

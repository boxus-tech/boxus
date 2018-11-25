import warnings
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Boolean, Text,\
                       ARRAY, dialects,\
                       delete, insert, update, select

from nanpy import SerialManager
from nanpy import ArduinoApi

from .dbase import DBase
from .utils import rev_dict

class Controllable(DBase):
    __abstract__ = True

    type_id = Column(Integer, nullable=False, default=0)
    control_id= Column(Integer, nullable=False)
    deactivated = Column(Boolean)

    name = Column(Text, nullable=False)
    description = Column(Text)
    arduino_port = Column(Text)

    pins = Column(dialects.postgresql.JSONB)

    supported_control_types = {
        0: 'native',
        1: 'arduino'
    }

    supported_types = {
        0: 'generic'
    }

    @contextmanager
    def arduino_api_scope(self):
        connection = SerialManager(device=self.arduino_port)
        arduino = ArduinoApi(connection=connection)

        try:
            yield arduino
        finally:
            connection.close()

    @property
    def control(self):
        return self.supported_control_types[self.type_id]

    @controll.setter
    def control(self, val):
        self.control_id = rev_dict(self.supported_control_types)[val]

    @property
    def type_name(self):
        return self.supported_types[self.type_id]

    @type_name.setter
    def type_name(self, val):
        self.type_id = rev_dict(self.supported_types)[val]

    def _check_status(self):
        if not self.deactivated:
            return True
        else:
            warnings.warn('Controlable device "%s" is deactivated' % self.description, Warning)
            return False

    def _check_type(self):
        if self.type_id in self.supported_types.keys():
            return True
        else:
            warnings.warn('Control of "%s" type are not yet implemented' % self.type_name, FutureWarning)
            return False

    def _check_control(self):
        if self.control_id in self.supported_control_types.keys():
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

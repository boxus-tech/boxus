import time
from couchdb.mapping import TextField

from .controllable import Controllable

class Device(Controllable):
    description = TextField()

    supported_types = [
        'generic',
        'relay'
    ]

    db_name = 'devices'

    def on(self):
        return self._send_control_sequence('on', self.type_name, False)

    def off(self):
        return self._send_control_sequence('off', self.type_name, False)

    def on_for(self, val, units='seconds'):
        assert units in [
                'second', 'seconds',
                'minute', 'minutes',
                'hour', 'hours',
                'day', 'days'
            ]

        delay = 0 # seconds

        if units in ['second', 'seconds']:
            delay = val
        elif units in ['minute', 'minutes']:
            delay = val*60
        elif units in ['hour', 'hours']:
            delay = val*60*60
        elif units in ['day', 'days']:
            delay = val*60*60*24

        self.on()
        time.sleep(delay)
        self.off()

    def _on_generic(self):
        self.digital_out(self.pins['power']['number'], 1)

    def _off_generic(self):
        self.digital_out(self.pins['power']['number'], 0)

    def _on_relay(self):
        self.digital_out(self.pins['power']['number'], 0)

    def _off_relay(self):
        self.digital_out(self.pins['power']['number'], 1)

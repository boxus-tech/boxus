import time

from .controllable import Controllable
from .utils        import *

class Device(Controllable):
    __tablename__ = 'devices'

    supported_types = [
        'generic',
        'relay'
    ]

    def on(self):
        return self._send_control_sequence('on', self.type_name, False)

    def off(self):
        return self._send_control_sequence('off', self.type_name, False)

    def on_for(self, n, units='seconds'):
        assert units in [
                'second', 'seconds',
                'minute', 'minutes',
                'hour',   'hours',
            ]

        delay = human_interval_to_seconds(n, units) # seconds

        self.on()
        time.sleep(delay)
        self.off()

    def _on_generic(self):
        self._digital_out(self.pins['power']['number'], 1)

    def _off_generic(self):
        self._digital_out(self.pins['power']['number'], 0)

    def _on_relay(self):
        self._digital_out(self.pins['power']['number'], 0)

    def _off_relay(self):
        self._digital_out(self.pins['power']['number'], 1)

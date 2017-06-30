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

    def _on_generic(self):
        self.digital_out(self.pins['power']['number'], 1)

    def _off_generic(self):
        self.digital_out(self.pins['power']['number'], 0)

    def _on_relay(self):
        self.digital_out(self.pins['power']['number'], 0)

    def _off_relay(self):
        self.digital_out(self.pins['power']['number'], 1)

from couchdb.mapping import TextField

from .controllable import Controllable

class Device(Controllable):
    description = TextField()

    supported_types = [
        'generic'
    ]

    db_name = 'devices'

    def on(self):
        return self.send_control_squence('on', self.type_name, False)

    def off(self):
        return self.send_control_squence('off', self.type_name, False)

    def on_generic(self):
        self.digital_out(self.pins['power']['number'], 1)

    def off_generic(self):
        self.digital_out(self.pins['power']['number'], 0)

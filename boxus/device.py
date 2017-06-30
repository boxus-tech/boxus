from couchdb.mapping import TextField, DictField

from .controllable import Controllable

class Device(Controllable):
    description = TextField()

    supported_types = [
        'generic'
    ]

    db_name = 'devices'

    def on(self):
        if self.check_type() and self.check_control():
            getattr(self, 'on_%s' % self.type_name)()
        else:
            return False

    def off(self):
        if self.check_type() and self.check_control():
            getattr(self, 'off_%s' % self.type_name)()
        else:
            return False
import yaml

from couchdb.client import Server

from .device import Device
from .sensor import Sensor

class DB(dict):

    server      = None
    sensors     = None
    readings    = None
    devices     = None

    config = {
        # TODO Server credentials are currently not used
        'server': {
          'host':   'localhost',
          'port':   5984
        },

        'schema': {
          'sensors_db':     'sensors',
          'readings_db':    'readings',
          'devices_db':     'devices'
        }
    }

    def __init__(self, config_path = None):
        self.server = Server()

        if config_path:
            self.config = yaml.load(open(config_path, 'r').read())

        if not all(db_name in self.server for db_name in self.config['schema'].values()):
            self.setup()

        self.connect()

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(DB, self).__setitem__(key, value)
        self.__dict__.update({ key: value })

    def connect(self):
        for db_name, attr_name in [['sensors_db', 'sensors'], ['readings_db', 'readings'], ['devices_db', 'devices']]:
            setattr(self, attr_name, self.server[self.config['schema'][db_name]])

    def setup(self):
        for db_name in ['sensors_db', 'readings_db', 'devices_db']:
            if self.config['schema'][db_name] not in self.server:
                self.server.create(self.config['schema'][db_name])

    def seed(self, seed_path):
        seed = yaml.load(open(seed_path, 'r').read())

        for db_name, Cls in [['sensors', Sensor], ['devices', Device]]:
            for r in seed[db_name]:
                new_r = Cls(self)

                for k in r:
                    new_r[k] = r[k]

                new_r.save()

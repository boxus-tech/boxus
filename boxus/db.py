import yaml

from couchdb.client import Server

class DB:

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

    def connect(self):
        self.sensors    = self.server[self.config['schema']['sensors_db']]
        self.readings   = self.server[self.config['schema']['readings_db']]
        self.devices    = self.server[self.config['schema']['devices_db']]

    def setup(self):
        if self.config['schema']['sensors_db'] not in self.server:
            self.server.create(self.config['schema']['sensors_db'])
        if self.config['schema']['readings_db'] not in self.server:
            self.server.create(self.config['schema']['readings_db'])
        if self.config['schema']['devices_db'] not in self.server:
            self.server.create(self.config['schema']['devices_db'])

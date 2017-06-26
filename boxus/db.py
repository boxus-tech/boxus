import yaml

from couchdb.client import Server

class DB(object):

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

    def connect(self):
        for db_name, attr_name in [['sensors_db', 'sensors'], ['readings_db', 'readings'], ['devices_db', 'devices']]:
            setattr(self, attr_name, self.server[self.config['schema'][db_name]])

    def setup(self):
        for db_name in ['sensors_db', 'readings_db', 'devices_db']:
            if self.config['schema'][db_name] not in self.server:
                self.server.create(self.config['schema'][db_name])

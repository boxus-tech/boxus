from couchdb.client import Server

class DB:

    server = None
    sensors = None
    measurements = None

    def __init__(self):
        self.server = Server()

    def connect(self):
        self.sensors = self.server['sensors']
        self.measurements = self.server['measurements']

    def setup(self):
        self.server.create('sensors')
        self.server.create('measurements')

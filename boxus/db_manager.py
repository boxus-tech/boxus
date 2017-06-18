import yaml

from .db     import DB

from .device import Device
from .sensor import Sensor

class DBManager:

    def seed(self, seed_path):
        db = DB()
        db.connect()

        seed = yaml.load(open(seed_path, 'r').read())

        for s in seed['sensors']:
            new_s = Sensor(db.sensors)

            for k in s:
                new_s[k] = s[k]

            new_s.save()

        for d in seed['devices']:
            new_d = Device(db.devices)

            for k in d:
                new_d[k] = d[k]

            new_d.save()

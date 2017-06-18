from boxus import DB
from boxus import Sensor

db = DB()
db.connect()

sensors = Sensor.all(db.sensors)

for s in sensors:
    s.read()

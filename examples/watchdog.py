from boxus import DB, Sensor

db = DB()

sensors = Sensor.all(db.sensors)

for s in sensors:
    s.read()

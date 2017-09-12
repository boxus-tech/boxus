from boxus import DB, Sensor

db = DB()

sensors = Sensor.all(db)

for s in sensors:
    s.read(True)

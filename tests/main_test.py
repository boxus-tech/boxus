from datetime import datetime
from boxus import DB, Manager, Sensor, Device, Reading

# def __init__(self):
#     self.db = DB()
#     self.db.setup()
#     self.db.connect()

def test_db_setup():
    db = DB()
    db.setup()
    db.connect()

    assert db.sensors is not None

def test_sensor_create():
    db = DB()
    db.connect()

    s = Sensor(db.sensors)
    s.description = 'Sensor description'
    s.id = 'test_sensor_id'
    s.save()

    assert isinstance(s.created_at, datetime)

def test_sensor_find_and_destroy():
    db = DB()
    db.connect()

    s0 = Sensor.find(db.sensors, 'test_sensor_id')
    assert s0 is not None

    s0.destroy()

    s1 = Sensor.find(db.sensors, 'test_sensor_id')
    assert s1 is None

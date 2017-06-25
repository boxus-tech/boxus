import os
import yaml

from datetime import datetime
from boxus import DB, Manager, Sensor, Device, Reading


##### Global functions #####
def conf_path(path):
    return os.path.dirname(__file__) + '/' + path

def drop_dbs():
    db = DB(conf_path('database.test.yml'))
    config = yaml.load(open(conf_path('database.test.yml'), 'r').read())

    for db_name in config['schema'].values():
        if db_name in db.server:
            del db.server[db_name]

##### Tests #####
def test_db_setup():
    drop_dbs()

    db = DB(conf_path('database.test.yml'))
    db.setup()
    db.connect()

    assert db.sensors is not None

def test_manager_seed():
    db = DB(conf_path('database.test.yml'))
    db.connect()

    manager = Manager(db)
    manager.seed(conf_path('seed.test.yml'))

    assert len(Sensor.all(db.sensors)) == 2

def test_sensor_create():
    db = DB(conf_path('database.test.yml'))
    db.connect()

    s = Sensor(db.sensors)
    s.description = 'Sensor description'
    s.id = 'test_sensor_id_0'
    s.save()

    assert isinstance(s.created_at, datetime)
    assert len(Sensor.all(db.sensors)) == 3

def test_sensor_find_and_destroy():
    db = DB(conf_path('database.test.yml'))
    db.connect()

    s0 = Sensor.find(db.sensors, 'test_sensor_id_0')
    assert s0 is not None

    s0.destroy()

    s1 = Sensor.find(db.sensors, 'test_sensor_id_0')
    assert s1 is None

def test_drop_dbs():
    drop_dbs()

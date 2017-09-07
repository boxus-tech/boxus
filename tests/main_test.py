import os
import yaml

from datetime import datetime
from boxus import DB, Manager, Sensor, Device, Reading, human_interval_to_seconds


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

    assert db.sensors is not None

def test_manager_seed():
    db = DB(conf_path('database.test.yml'))

    db.seed(conf_path('seed.test.yml'))

    assert len(Sensor.all(db)) == 3

def test_sensor_create():
    db = DB(conf_path('database.test.yml'))

    s = Sensor(db)
    s.description = 'Sensor description'
    s.id = 'test_sensor_id_0'
    s.save()

    assert isinstance(s.created_at, datetime)
    assert len(Sensor.all(db)) == 4

def test_sensor_find_and_destroy():
    db = DB(conf_path('database.test.yml'))

    s0 = Sensor.find(db, 'test_sensor_id_0')
    assert s0 is not None

    s0.destroy()

    s1 = Sensor.find(db, 'test_sensor_id_0')
    assert s1 is None

def test_sensor_read():
    db = DB(conf_path('database.test.yml'))

    s1 = Sensor.find(db, 'test_sensor_id_1')
    assert s1 is not None

    result = s1.read()
    assert result is None

def test_deactivated_sensor_read():
    db = DB(conf_path('database.test.yml'))

    s3 = Sensor.find(db, 'test_sensor_id_3')
    assert s3 is not None

    assert s3._check_status() is False

    result = s3.read()
    assert result is None

def test_sensor_save_readings():
    db = DB(conf_path('database.test.yml'))

    s1 = Sensor.find(db, 'test_sensor_id_1')
    s1.save_readings([1, 2])

    readings = s1.readings()
    assert len(readings) == 1

    readings = s1.readings_for(2, 'days')
    assert len(readings) == 1

def test_sensor_serialize():
    db = DB(conf_path('database.test.yml'))

    s1 = Sensor.find(db, 'test_sensor_id_1')
    assert type(s1.to_json()) is str

def test_utils():
    assert human_interval_to_seconds(1, 'day')      == 60*60*24
    assert human_interval_to_seconds(15, 'seconds') == 15
    assert human_interval_to_seconds(2, 'weeks')    == 60*60*24*7*2


def test_drop_dbs():
    drop_dbs()

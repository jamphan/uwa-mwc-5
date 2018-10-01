import pytest
import os
from datetime import datetime
import time
import random
import collections

from trashyApp.database.jsonDb import jsonDb

TEST_DB_FILE = 'test.json'

def clean_up():
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_jsonDb_addBin():

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_1')
    db.add_bin('test_bin_2', position=(10,20))
    data = db.data

    assert 'test_bin_1' in data['bins']
    assert 'test_bin_2' in data['bins']
    assert data['bins']['test_bin_2']['lat'] == 10
    assert data['bins']['test_bin_2']['long'] == 20

    # Update the data to see that the changes are recognised
    db.add_bin('test_bin_2', position=(20, 30))
    data = db.data
    assert 'test_bin_2' in data['bins']
    assert data['bins']['test_bin_2']['lat'] == 20
    assert data['bins']['test_bin_2']['long'] == 30

    clean_up()

def test_ModExistingDb():

    db_before = jsonDb(path=TEST_DB_FILE)
    db_before.add_bin('test_bin_1')
    db = jsonDb(path=TEST_DB_FILE)
    data = db.data

    assert 'test_bin_1' in data['bins']

    clean_up()

def test_getAllBins():

    db = jsonDb(path=TEST_DB_FILE)
    
    for i in range(10):
        db.add_bin('test_bin_{:d}'.format(i))

    all_bins = db.get_all_bins()
    
    assert len(all_bins) == 10
    for i in range(10):
        assert 'test_bin_{:d}'.format(i) in all_bins

    clean_up()

def test_getBinInfo():

    db = jsonDb(path=TEST_DB_FILE)

    db.add_bin('test_bin_99', position=(10, 20), capacity=100, fill_threshold=13)
    bin_info = db.get_info_bin('test_bin_99')

    # Add some noise for the test
    for i in range(10):
        db.add_bin('test_bin_{:d}'.format(i))

    # Test values are correct
    assert bin_info['lat'] == 10
    assert bin_info['long'] == 20
    assert bin_info['depth'] == 100
    assert bin_info['threshold'] == 13

    # Test values are correct (method 2)
    assert db.get_info_bin('test_bin_99', key='lat') == 10
    assert db.get_info_bin('test_bin_99', key='long') == 20
    assert db.get_info_bin('test_bin_99', key='depth') == 100
    assert db.get_info_bin('test_bin_99', key='threshold') == 13

    clean_up()

def test_automaticallySetThreshold():

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_99', position=(10, 20), capacity=100)
    assert db.get_info_bin('test_bin_99', key='threshold') == 100

    clean_up()

def test_verifyIsBin():
    """ Test to see if DB can properly determine if a given ID is 
    a bin or not
    """

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_99', position=(10, 20), capacity=100)

    assert not(db.is_bin('not_a_bin'))
    assert db.is_bin('test_bin_99')

    clean_up()

def test_jsonDB_badBinRequest():
    """ Test that None's are retured for information that doesn't exist
    """

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_99')

    assert db.is_bin('test_bin_99')
    assert db.get_info_bin('test_bin_99', key='lat') is None
    assert db.get_info_bin('test_bin_99', key='long') is None
    assert db.get_info_bin('test_bin_99', key='depth') is None
    assert db.get_info_bin('test_bin_99', key='threshold') is None

    assert db.get_info_bin("not_a_bin") is None
    assert db.get_info_bin('not_a_bin', key='lat') is None

    clean_up()

def test_jsonDB_addSensor():
    """ Test JSONDB adding a sensor
    """

    db = jsonDb(path=TEST_DB_FILE)
    db.add_sensor('test_sensor_1')

    assert db.is_sensor('test_sensor_1')
    assert not(db.is_sensor('test_sensor_2'))

    db.add_sensor('test_sensor_2', sensor_type='Arduino')
    assert db.is_sensor('test_sensor_2')
    assert db.get_info_sensor('test_sensor_2', key='type') == 'Arduino'

    clean_up()
    
def test_jsonDB_linkSensor():
    """ Test that the db can properly link Sensor to DB
    """

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_1')
    db.add_sensor('test_sensor_1', linked_to='test_bin_1')

    assert db.is_sensor('test_sensor_1')
    assert db.is_bin('test_bin_1')
    assert db.is_bin(db.get_info_sensor('test_sensor_1', key='bin_number'))

    clean_up()

def test_jsonDb_addSensorData():
    """ Basic test for adding data"""

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_1')
    db.add_sensor('test_sensor_1', linked_to='test_bin_1')

    db.add_data('test_sensor_1', 10)

    d = db.get_data_bin('test_bin_1')
    assert d['values'] == [10]

    time.sleep(1)
    db.add_data('test_sensor_1', 20)
    d = db.get_data_bin('test_bin_1')
    assert d['values'] == [10, 20]
    assert d['recorded_by'][-1] == 'test_sensor_1'

    clean_up()

def test_jsonDb_addDiagnosticData():

    db = jsonDb(path=TEST_DB_FILE)
    db.add_sensor('test_sensor_1', linked_to='test_bin_1')

    db.add_diagnostics('test_sensor_1', 10)
    d = db.get_data_sensor('test_sensor_1')
    assert d['diagnostics'] == [10]

    clean_up()

def test_jsonDb_LargeNetwork():
    """ Test with large number of sensors
    """

    N_ELEMENTS = 10
    N_DATA_PTS = 20

    db = jsonDb(path=TEST_DB_FILE)

    for i in range(N_ELEMENTS):
        bin_id = "test_bin_{:d}".format(i)
        pos = (random.uniform(-180, 180), random.uniform(-90, 90))
        cap = random.uniform(10,100)
        db.add_bin(bin_id, position=pos, capacity=cap)
    
        sens_id = "test_sensor_{:d}".format(i)
        db.add_sensor(sens_id, linked_to=bin_id)

    assert len(db.get_all_bins()) == N_ELEMENTS
    assert len(db.get_all_sensors()) == N_ELEMENTS

    expected_data = collections.defaultdict(list)
    expected_diag = collections.defaultdict(list)

    for i in range(N_DATA_PTS):

        rand_sensor_id = random.randint(0, N_ELEMENTS-1)
        sens_id = "test_sensor_{:d}".format(rand_sensor_id)

        rand_data = random.uniform(-100, 100)
        rand_diag = random.uniform(-100, 100)

        expected_data[sens_id].append(rand_data)
        expected_diag[sens_id].append(rand_diag)

        db.add_data(sens_id, rand_data)
        db.add_diagnostics(sens_id, rand_diag)

    # Check answers
    for i in range(N_ELEMENTS):
        bin_id = "test_bin_{:d}".format(i)
        sens_id = "test_sensor_{:d}".format(i)

        actual = db.get_data_bin(bin_id)
        if actual is None:
            assert len(expected_data[sens_id]) == 0
        else:
            assert actual['values'] == expected_data[sens_id]
            assert len(actual['timestamps']) == len(expected_data[sens_id])

        actual = db.get_data_sensor(sens_id)
        if actual is None:
            assert len(expected_diag[sens_id]) == 0
        else:
            assert actual['diagnostics'] == expected_diag[sens_id]
            assert len(actual['timestamps']) == len(expected_diag[sens_id])

    clean_up()
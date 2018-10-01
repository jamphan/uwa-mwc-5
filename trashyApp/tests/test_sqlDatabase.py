import pytest
import os

from trashyApp.database.sqliteDb import SQLite3Db

@pytest.fixture(scope='module')
def basedb():
    """ Create the base database to test from. Ensure that we do not remove
    _test_data entries. It's oaky to add more data though!
    """

    TEST_PATH = 'basedb_test.db'

    _test_data_bin = { # Bin_Id: [(lat, lon), capacity, fill_threshold]
        'perth_bin_1': [(-31.9505, 115.8605), 100, 80],
        'perth_bin_2': [(-31.9512, 115.8503), 120, 110]
        # TODO: Case where one property is missing
    }

    _test_data_sensor = { # Sensor_Id: [type, linked_to]
        'sensor_1': ['Arduino', 'perth_bin_1'],
        'sensor_2_noLink': ['RPi', None],
        'sensor_3_noProperties': [None, None]
    }
    # Start fresh
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)

    # Create a clean database with fixed test data
    db = SQLite3Db(path=TEST_PATH, build=True)

    # Add the bin data
    for bin_id, bin_data in _test_data_bin.items():
        lat = bin_data[0][0]
        lon = bin_data[0][1]
        cap = bin_data[1]
        thr = bin_data[2]
        db.add_bin(bin_id, position=(lat,lon), capacity=cap, fill_threshold=thr)

    # Add the sensor data
    for sensor_id, sensor_data in _test_data_sensor.items():
        sens_type = sensor_data[0]
        sens_link = sensor_data[1]
        db.add_sensor(sensor_id, sensor_type=sens_type, linked_to=sens_link)

    yield db

    # Clean up
    db.close()
    os.remove(TEST_PATH)

def test_sqlDatabase_noReturn(basedb):
    """ Check that requesting an element that does not exist in the database
    returns None
    """

    assert basedb.get_info_bin('not_a_bin') is None
    assert basedb.get_info_sensor('not_a_sensor') is None

def test_sqlDatabase_addElements(basedb):
    """ Check that the elements (bins and sensors) have been correctly
    added
    """

    # Check that the format is correct
    assert basedb.get_info_bin('perth_bin_1') == {'bin_id': 'perth_bin_1',
                                                  'latitude': -31.9505,
                                                  'longitude': 115.8605,
                                                  'capacity': 100,
                                                  'fill_threshold': 80}

    # Check that a record exist for valid sensors
    assert basedb.get_info_sensor('sensor_1') == {'sensor_id': 'sensor_1',
                                                  'type': 'Arduino',
                                                  'linked_to': 'perth_bin_1'}

    assert basedb.get_info_sensor('sensor_2_noLink') == {'sensor_id': 'sensor_2_noLink',
                                                         'type': 'RPi',
                                                         'linked_to': None}

    assert basedb.get_info_sensor('sensor_3_noProperties') == {'sensor_id': 'sensor_3_noProperties',
                                                               'type': None,
                                                               'linked_to': None}

def test_sqlDatabase_isCheckMethods(basedb):
    """ Check the methods is_sensor() and is_bin() works
    """

    assert basedb.is_bin('perth_bin_1')         # Check if can pick an actual bin
    assert not(basedb.is_bin('not_a_bin'))      # Check it detects non-bins
    assert basedb.is_sensor('sensor_1')         # Check it can pick an actual sensor
    assert not(basedb.is_sensor('not_a_sensor'))# Check it detects non-bins

def test_sqlDatabase_repeatedAddFails(basedb):
    """ Check that the database does not permit adding non-unique bin labels
    """

    assert basedb.add_bin('perth_bin_1') == False
    assert basedb.add_sensor('sensor_1') == False
    assert basedb.add_sensor('sensor_2_noLink') == False

def test_sqlDatabase_getAllBinsMethod(basedb):

    expected = ['perth_bin_1', 'perth_bin_2']
    actual = basedb.get_all_bins()
    assert len(expected) == len(actual)

    for bin_id in actual:
        assert bin_id in expected

    for bin_id in expected:
        assert bin_id in actual
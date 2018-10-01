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

    yield db

    # Clean up
    db.close()
    os.remove(TEST_PATH)

def test_sqlDatabase_noReturn(basedb):
    """ Check that requesting a bin that does not exist returns None
    """

    assert basedb.get_info_bin('not_a_bin') is None

def test_sqlDatabase_addElements(basedb):
    """ Check that the elements (bins and sensors) have been correctly
    added
    """

    # Check that a record does exist
    assert basedb.get_info_bin('perth_bin_1') is not None

    # Check that the format is correct
    assert basedb.get_info_bin('perth_bin_1') == {'bin_id': 'perth_bin_1',
                                                  'latitude': -31.9505,
                                                  'longitude': 115.8605, 
                                                  'capacity': 100, 
                                                  'fill_threshold': 80}

def test_sqlDatabase_isBinMethod(basedb):
    """ Check the method is_bin() works
    """

    # Check if can pick an actual bin
    assert basedb.is_bin('perth_bin_1')

    # Check it detects non-bins
    assert not(basedb.is_bin('not_a_bin'))

def test_sqlDatabase_repeatedAddFails(basedb):
    """ Check that the database does not permit adding non-unique bin labels
    """

    assert basedb.add_bin('perth_bin_1') == False

def test_sqlDatabase_getAllBinsMethod(basedb):

    expected = ['perth_bin_1', 'perth_bin_2']
    actual = basedb.get_all_bins()
    assert len(expected) == len(actual)
    
    for bin_id in actual:
        assert bin_id in expected

    for bin_id in expected:
        assert bin_id in actual
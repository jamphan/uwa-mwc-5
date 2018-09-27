import pytest
import os

from app.database.jsonDb import jsonDb

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
    assert bin_info['capacity'] == 100
    assert bin_info['threshold'] == 13

    # Test values are correct (method 2)
    assert db.get_info_bin('test_bin_99', key='lat') == 10
    assert db.get_info_bin('test_bin_99', key='long') == 20
    assert db.get_info_bin('test_bin_99', key='capacity') == 100
    assert db.get_info_bin('test_bin_99', key='threshold') == 13

    clean_up()

def test_automaticallySetThreshold():

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_99', position=(10, 20), capacity=100)
    assert db.get_info_bin('test_bin_99', key='threshold') == 100

    clean_up()
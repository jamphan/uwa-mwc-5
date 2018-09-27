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

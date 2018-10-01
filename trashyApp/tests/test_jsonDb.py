import pytest
import os
from datetime import datetime
import time
import random
import collections

from trashyApp.database.jsonDb import jsonDb

TEST_DB_FILE = 'test.json'
N_TEST_ELEMENTS = 10
N_TEST_DATAPTS = 20

class TestObj(object):

    def __init__(self, db):

        self._db = db

    @property
    def db(self):
        return self._db

@pytest.fixture(scope="module", autouse=True)
def transact():

    TEST_DB_FILE = 'test.json'
    
    db = jsonDb(path=TEST_DB_FILE)
    tObj = TestObj(db)
    
    for i in range(N_TEST_ELEMENTS):
        bin_id = "test_bin_{:d}".format(i)

        pos = (random.uniform(-180, 180), random.uniform(-90, 90))
        cap = random.uniform(10,100)
        db.add_bin(bin_id, position=pos, capacity=cap)
    
        sens_id = "test_sensor_{:d}".format(i)
        db.add_sensor(sens_id, linked_to=bin_id)

    expected_data = collections.defaultdict(list)
    expected_diag = collections.defaultdict(list)

    for i in range(N_TEST_DATAPTS):

        rand_sensor_id = random.randint(0, N_TEST_ELEMENTS-1)
        sens_id = "test_sensor_{:d}".format(rand_sensor_id)

        rand_data = random.uniform(-100, 100)
        rand_diag = random.uniform(-100, 100)

        expected_data[sens_id].append(rand_data)
        expected_diag[sens_id].append(rand_diag)

        db.add_data(sens_id, rand_data)
        db.add_diagnostics(sens_id, rand_diag)

    tObj.expected_data = expected_data

    yield tObj

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_numberElements(transact):

    assert len(transact.db.get_all_bins()) == N_TEST_ELEMENTS
    assert len(transact.db.get_all_sensors()) == N_TEST_ELEMENTS

def test_elementLinks(transact):

    for i in range(N_TEST_ELEMENTS):
        sens_id = "test_sensor_{:d}".format(i)

        assert transact.db.is_sensor(sens_id)
        linked_bin = transact.db.get_info_sensor(sens_id, key='bin_number')
        assert transact.db.is_bin(linked_bin)
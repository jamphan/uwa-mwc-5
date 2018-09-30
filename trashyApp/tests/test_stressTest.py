import pytest
import time
import os

from trashyApp.database.jsonDb import jsonDb

TEST_DB_FILE = 'test.json'

def clean_up():
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('\n\n\t{:s} function took {:.3f} ms\n\n'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

@timing
def ignore_test_database_stresstest():

    db = jsonDb(path=TEST_DB_FILE)
    db.add_bin('test_bin_1')
    db.add_sensor('test_sensor_1', linked_to='test_bin_1')

    N_DATA = 10
    for i in range(N_DATA):
        db.add_data('test_sensor_1', i)

    d = db.get_data_bin('test_bin_1')
    assert len(d['bin_values']) == N_DATA

    clean_up()
import pytest
import os

from trashyApp.database.sqliteDb import SQLite3Db

TEST_PATH = 'test.db'

def test_sqlite3_basic():
    
    db = SQLite3Db(path=TEST_PATH, build=True)
    db.add_bin('test_bin_2', position=(10,20))
    for i in db.get_info_bin('test_bin_2', key='latitude'):
        print(i)

    db.close()
    os.remove(TEST_PATH)


import pytest

from trashyApp.database.sqliteDb import SQLite3Db

def test_sqlite3_basic():
    
    db = SQLite3Db(path='test.db', build=True)
    db.add_bin('test_bin_2', position=(10,20))
    for i in db.get_info_bin('test_bin_2', key='latitude'):
        print(i)


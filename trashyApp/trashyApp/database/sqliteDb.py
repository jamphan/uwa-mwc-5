import sqlite3
import os

from . import BaseBinDb

class SQLite3Db(BaseBinDb):

    def __init__(self, path='database.db', build=False):

        self._path = path

        if build:
            if os.path.exists(self._path):
                os.remove(self._path)

            conn = sqlite3.connect(self._path)
            self._conn = conn
            self._schema_build()

        # Check if database exists
        conn = sqlite3.connect(self._path)
        self._conn = conn

    @property
    def conn(self):
        return self._conn

    @property
    def cursor(self):
        return self._conn.cursor()

    def committed(func):

        def wrapper_committed(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.conn.commit()

        return wrapper_committed

    @committed
    def _schema_build(self):

        self.cursor.execute("""CREATE TABLE Item
        (
            id INTEGER primary key autoincrement
            ,label TEXT
            ,type TEXT
            ,latitude REAL
            ,longitude REAL
        )
        """)

        # self.cursor.execute("""CREATE TABLE Sensor
        # (
        #     id INTEGER primary key autoincrement
        #     ,label TEXT
        #     ,type TEXT
        #     ,ItemId INTEGER
        #     ,FOREIGN KEY(ItemId) REFERENCES 
        # )
        # """)

    @committed
    def add_bin(self, bin_id, position=None, capacity=None, fill_threshold=None):
        
        if isinstance(position, tuple) and len(position) == 2:
            lat, long = position
        else:
            lat = None
            long = None
        vals = (bin_id, 'bin', lat, long, )

        self.cursor.execute("""INSERT INTO Item
        (
            label
            ,type
            ,latitude
            ,longitude
        )
        VALUES
        (
            ?
            ,?
            ,?
            ,?
        )
        """, vals)

    def get_info_bin(self, bin_id, key=None):
        
        if key is not None:
            vals = (key, bin_id, )
            return self.cursor.execute("""SELECT ? FROM Item WHERE label = ?""", vals)
        else:
            vals = (bin_id, )
            return self.cursor.execute("""SELECT * FROM Item WHERE label = ?""", vals)
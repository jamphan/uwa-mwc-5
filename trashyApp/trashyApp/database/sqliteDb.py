from __future__ import with_statement

import sqlite3
import os
import collections
from datetime import datetime
from contextlib import closing

from . import BaseBinDb

class SQLite3Db(BaseBinDb):
    """ A sql implementation of the base bin database ABC

    Args:
        path (str, optional): The path that the database should be looaded from
            defaults to database.db relative to the instance
        build (bool, optional): Specify True to overwrite any existing data and
            rebuild the entire schema

    Attributes:
        conn (sqlite3.connection): The open sqlite connection
    """

    def __init__(self, path='./database.db', build=False, time_format='%Y-%m-%d %H:%M:%S'):

        self._path = path
        self._time_format = time_format

        # If the user requests to build, we will clear any existing
        # db files and make a new file
        if build:
            if os.path.exists(self._path):
                os.remove(self._path)

            conn = sqlite3.connect(self._path)
            self._conn = conn
            self._schema_build()

        # Check if database exists
        conn = sqlite3.connect(self._path)
        self._conn = conn

        # TODO: Check if schema is valid

    @property
    def conn(self):
        return self._conn

    def close(self):
        """ Cleanly close the database
        """

        self._conn.close()

    def committed(func):
        """ All queries in this class should use this decorator, as it will
        correctly wrap the cursor and commit.

        Once decorated, the self.cursor property will be available for use.

        Note because this is set to use the context with an attribute,
        we cannot nest committed functions (the nested function will
        close self.cursor, and the parent function will fail)

        Todo:
            investigate nested funcitonality
        """

        def wrapper_committed(self, *args, **kwargs):
            with closing(self._conn.cursor()) as self.cursor:
                return func(self, *args, **kwargs)
            self.conn.commit()

        return wrapper_committed

    @committed
    def _schema_build(self):
        """ Builds the database schema
        """

        # TODO: Add unique for label
        self.cursor.execute("""CREATE TABLE Item
        (
            id INTEGER primary key autoincrement
            ,label TEXT
            ,type TEXT
            ,latitude REAL
            ,longitude REAL
            ,capacity REAL
            ,fill_threshold REAL
        )
        """)

        self.cursor.execute("""CREATE TABLE Sensor
        (
            id INTEGER primary key autoincrement
            ,label TEXT
            ,type TEXT
            ,ItemId INTEGER
            ,FOREIGN KEY(ItemId) REFERENCES Item(id)
        )
        """)

        self.cursor.execute("""CREATE TABLE ItemData
        (
            id INTEGER primary key autoincrement
            ,RecordBySensorId INTEGER
            ,ItemId INTEGER
            ,timestamp DATETIME
            ,measurement TEXT
            ,value REAL
            ,FOREIGN KEY(RecordBySensorId) REFERENCES Sensor(id)
            ,FOREIGN KEY(ItemId) REFERENCES Item(Id)
        )
        """)

    @committed
    def add_bin(self, bin_id, position=None, capacity=None, fill_threshold=None):
        """ Adds a bin to the database

        Args:
            bin_id (str): the bin identifier (label) to add to the database
            position (tuple, default=None):

        Returns:
            bool: True on success, False otherwise
        """

        # TODO: Permit a bulk insert using .executemany()
        #       - Check that len of all parameters are equal

        # Check if the label already exists
        # TODO: Check if _schema_build() has unique constraint
        self.cursor.execute("""SELECT id FROM Item WHERE label = ?""", (bin_id,))
        if self.cursor.fetchone() is not None:
            return False

        # The lat, long need to default to two serparate params
        if isinstance(position, tuple) and len(position) == 2:
            lat, long = position
        else:
            lat = None
            long = None

        # Prepare the fill
        vals = (bin_id, 'bin', lat, long, capacity, fill_threshold)

        self.cursor.execute("""INSERT INTO Item (label, type, latitude, longitude, capacity, fill_threshold)
        VALUES(?,?,?,?,?,?)""", vals)

        return True

    @committed
    def get_info_bin(self, bin_id):
        """ Returns the information for a single bin_id

        Note:
            We do not need to check for multiple records as there is a unique
            constraint on the label. We only need to check for no results

        Args:
            bin_id (str): The bin to request information for

        Returns:
            dict: With keys ['bin_id', 'latitude', 'longitude', 'capacity', 'fill_threshold']
            None: if any errors
        """

        vals = (bin_id, )
        results = self.cursor.execute("""SELECT * FROM Item WHERE label = ?""", vals)

        # Do a quick check that we don't have an empty result set
        all_results = [x for x in results]
        if len(all_results) == 0:
            return None
        else:
            ret = dict(
                bin_id=all_results[0][1],
                latitude=all_results[0][3],
                longitude=all_results[0][4],
                capacity=all_results[0][5],
                fill_threshold=all_results[0][6]
            )

        return ret

    @committed
    def is_bin(self, test_id):
        """ Test whether the request id is a bin or not

        Args:
            test_id (str): The item to test

        Returns:
            bool: True if test_id is a bin in the database, False otherwise
        """

        vals = (test_id, )
        self.cursor.execute("""SELECT id FROM Item WHERE label = ?""", vals)
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False

    @committed
    def get_all_bins(self):
        """ Get all the ids of the bins registerd in database

        Returns:
            list: A list of all bin ids
        """

        results = self.cursor.execute("""SELECT label FROM Item""")
        all_results = [x[0] for x in results]
        return all_results

    @committed
    def add_sensor(self, sensor_id, sensor_type=None, linked_to=None):
        """Add a sensor to the database

        Returns:
            bool: True on success, False otherwise
        """

        # TODO: Permit a bulk insert using .executemany()
        #       - Check that len of all parameters are equal

        # Check that the sensor id doesn't already exist
        self.cursor.execute("""SELECT id FROM Sensor WHERE label = ?""", (sensor_id,))
        if self.cursor.fetchone() is not None:
            return False

        if linked_to is not None:
            # Check if the rqeuested item to link to exists
            self.cursor.execute("""SELECT id FROM Item WHERE label = ?""", (linked_to,))
            item = self.cursor.fetchone()
            if item is None:
                return False
            else:
                item_id = item[0]
        else:
            item_id = None

        # Prepare the fill
        vals = (sensor_id, sensor_type, item_id, )

        self.cursor.execute("""INSERT INTO Sensor (label, type, ItemId)
        VALUES(?,?,?)""", vals)

        return True

    @committed
    def get_info_sensor(self, sensor_id):

        vals = (sensor_id, )
        results = self.cursor.execute("""SELECT [S].[label], [S].[type], [I].[Label] FROM Sensor as [S]
        LEFT JOIN Item as [I] on [S].[ItemId] = [I].[Id]
        WHERE [S].[label] = ?""", vals)

        # Do a quick check that we don't have an empty result set
        all_results = [x for x in results]
        if len(all_results) == 0:
            return None

        ret = dict(
            sensor_id=all_results[0][0],
            type=all_results[0][1],
            linked_to=all_results[0][2],
        )

        return ret

    @committed
    def is_sensor(self, test_id):

        """ Test whether the request id is a sensor or not

        Args:
            test_id (str): The item to test

        Returns:
            bool: True if test_id is a sensor in the database, False otherwise
        """

        vals = (test_id, )
        self.cursor.execute("""SELECT id FROM Sensor WHERE label = ?""", vals)
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False

    @committed
    def get_all_sensors(self):
        """ Get all the ids of the sensors registerd in database

        Returns:
            list: A list of all sensor ids
        """

        results = self.cursor.execute("""SELECT label FROM Sensor""")
        all_results = [x[0] for x in results]
        return all_results

    @committed
    def add_data(self, sensor_id, value, field='values', timestamp=None):
        """ Adds data recorded by a sensor to the database

        Args:
            sensor_id (str): The sensor label used
            value (float): The value to record
            field (str, optional): The measurement column to record it as. Note 
                that the database does not maintain referential integrity over
                this column, and it is up to the caller to ensure consistent
                usage of this column. Defaults to 'values'
            timestamp (datetime, optional): Time to record against. Defaults to
                time of call
        
        Returns:
            bool: True if successful, False otherwise
        """

        # TODO: Permit executemany

        # check that sensor is valid
        # TODO: Do we really need this? the WHERE condition in the INSERT 
        #       statement should filter any invalid sensor ids out. Only
        #       really useful for returns
        self.cursor.execute("""SELECT id FROM Sensor WHERE label = ?""", (sensor_id,))
        sensor_id = self.cursor.fetchone()
        if sensor_id is None:
            return False
        else:
            sensor_id = sensor_id[0]

        if timestamp is None:
            timestamp = datetime.now()
        elif not(isinstance(timestamp, datetime)):
            return False

        vals = (sensor_id, timestamp, field, value, sensor_id,)
        self.cursor.execute("""INSERT INTO ItemData (RecordBySensorId, ItemId, timestamp, measurement, value)
        select ?,[itm].[id],?,?,?
        from Sensor as [sen]
        left join Item as [itm] on [itm].[Id] = [sen].[ItemId]
        where 
            [sen].[id] = ?
        """, vals)

        return True

    @committed
    def get_data_item(self, item_label, measurement='%'):
        """ Get data recorded against an id

        Args:
            item_label (str): The item to fetch data for
            measurement (string, optional): A particular measurement to get.
                see add_data. Defaults to all measurement types with glob '%'

        Returns:
            dict: Dictionary with keys 'timestamp', 'measurement', 'value', and 
                'recorded_by'. Each of these keys are list-valued.
        """

        vals = (item_label, measurement, )
        ret = collections.defaultdict(list)
        for row in self.cursor.execute("""
            SELECT [Data].[Timestamp], [Data].[measurement], [Data].[Value], [Sn].[label]
            FROM ItemData as [Data]
            INNER JOIN Item as [It] on [It].[Id] = [Data].[ItemId]
            INNER JOIN Sensor as [Sn] on [Sn].[Id] = [Data].[RecordBySensorId]
            WHERE [It].[label] = ? AND [Data].[measurement] LIKE ?
        """, vals):
            ret['timestamp'].append(row[0])
            ret['measurement'].append(row[1])
            ret['value'].append(row[2])
            ret['recorded_by'].append(row[3])

        return ret





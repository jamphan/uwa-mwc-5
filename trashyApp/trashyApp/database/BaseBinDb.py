""" Abstract base class for the Bin Database

This class is to guarantee that the database will provide the following
class methods:

    - add_bin
    - add_sensor
    - get_data_bin
    - get_data_sensor
    - get_info_bin
    - get_info_sensor
    - get_all_bins
    - get_all_sensors
"""

import abc

class BaseBinDb(object):

    @property
    @abc.abstractmethod
    def data(self):
        """ Returns all the data stored in the database
        """

        pass

    @abc.abstractmethod
    def add_bin(self, bin_id, position=None, capacity=None, fill_threshold=None):
        """ Adds a bin to the database

        Args:
            bin_id (str): The unique bin identifier
            position (tuple, 2): The lat, long of the bin
            capacity (float): The capacity of the bin
            fill_threshold (float): The threshold of the bin before it is full
                If fill_threshold is None, but capacity > 0 then it the 
                threshold is automatically set to the capacity
        """
        pass
    
    @abc.abstractmethod
    def add_sensor(self, sensor_id, sensor_type=None, linked_to=None):
        pass

    @abc.abstractmethod
    def get_data_bin(self, bin_id, starting=None, ending=None):
        pass

    @abc.abstractmethod
    def get_data_sensor(self, sensor_id, starting=None, ending=None):
        pass

    @abc.abstractmethod
    def get_info_bin(self, bin_id, key=None):
        """ Returns the bin information for a particular bin

        Args:
            bin_id (str): The bin to get information for
            key (str, default=None): this will get a particular piece of 
                                     information
                relevant to the bin. Available keys are:
                    - lat (float): The latitude of the bin
                    - long (float): The longitude of the bin
                    - capacity (float): The capacity of the bin
                    - threshold (float): The threshold for filled bins

        Returns:
            None: If there are any key errors
            dict: If key = None
            float: If key is not none and there are no key errors
        """
        pass

    @abc.abstractmethod
    def get_info_sensor(self, sensor_id, key=None):
        """ Returns the sensor information for a particular sensor

        Args:
            sensor_id (str): The sensor to get information for
            key (str, default=None): this will get a particular piece of 
                information relevant to the sensor. Available keys are:
                    - type (str): The latitude of the bin
                    - linked_to (str): The bin_id that it is sensing

        Returns:
            None: If there are any key errors
            dict: If key = None
            float: If key is not none and there are no key errors
        """

        pass

    @abc.abstractmethod
    def get_all_bins(self):
        """ Get all the ids of the bins registerd in database

        Returns:
            list: A list of all bin ids
        """
        pass

    @abc.abstractmethod
    def get_all_sensors(self):
        """ Get all the ids of the sensors registerd in database

        Returns:
            list: A list of all sensors ids
        """
        pass

    @abc.abstractmethod
    def is_bin(self, test_id):
        """ Test whether the request id is a bin or not

        Args:
            test_id (str): The item to test

        Returns:
            True: if test_id is a bin in the database
            False: Otherwise
        """
        pass

    @abc.abstractmethod
    def is_sensor(self, test_id):
        """ Test whether the request id is a sensor or not

        Args:
            test_id (str): The item to test

        Returns:
            True: if test_id is a sensor in the database
            False: Otherwise
        """
        pass

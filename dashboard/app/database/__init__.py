import abc

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
        pass

    @abc.abstractmethod
    def get_info_sensor(self, sensor_id, key=None):
        pass

    @abc.abstractmethod
    def get_all_bins(self):
        pass

    @abc.abstractmethod
    def get_all_sensors(self):
        pass

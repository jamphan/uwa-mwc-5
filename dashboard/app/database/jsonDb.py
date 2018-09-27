import os
import json

from app.database import BaseBinDb

class jsonDb(BaseBinDb):

    def __init__(self, path='database.json'):

        self._path = path

        if os.path.exists(self._path):
            try:
                with open(self._path, 'r') as fd:
                    data = json.load(fd)
            except Exception:
                print("unable to load existing data")
                fd = open(self._path, 'w')
                json.dump({}, fd)
                fd.close()
        else:
            fd = open(self._path, 'w')
            json.dump({}, fd)
            fd.close()

    def _update(self, update_with):
        data = self.data

        for k, v in update_with.items():
            if k not in data:
                data.update(update_with)
            else:
                data[k].update(v)

        with open(self._path, 'w') as f:
            json.dump(data, f)

    @property
    def data(self):
        
        with open(self._path, 'r') as fd:
            data = json.load(fd)

        return data

    def add_bin(self, bin_id, position=None, capacity=None, fill_threshold=None):
        """ Adds a bin to the database
        """
        bin_obj = dict()
        
        if isinstance(position, tuple) and len(position) == 2:
            lat, long = position
            bin_obj["lat"] = lat
            bin_obj["long"] = long

        if capacity is not None:
            bin_obj["capacity"] = capacity

        if fill_threshold is not None:
            bin_obj["threshold"] = fill_threshold

        self._update({"bins": {bin_id: bin_obj}})
    
    def add_sensor(self, sensor_id, sensor_type=None, linked_to=None):
        
        sens_obj = dict()

        sens_obj["sensor_type"] = sensor_type

    def get_data_bin(self, bin_id, starting=None, ending=None):
        pass

    def get_data_sensor(self, sensor_id, starting=None, ending=None):
        pass

    def get_info_bin(self, bin_id):
        pass

    def get_info_sensor(self, sensor_id):
        pass

    def get_all_bins(self):
        pass

    def get_all_sensors(self):
        pass

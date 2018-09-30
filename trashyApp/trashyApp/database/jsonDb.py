import os
import json
from datetime import datetime

from trashyApp.database import BaseBinDb

def recursive_dict_update(dst, src):
    """ Update dst (dict) with src (dict). 
    
    This update method will:
        - Add a key if the key does not exist in dst but does in src
        - Append to the key if the key exists in dst and src and both are dict
            typed
        - Overwrite the key if the key exists in both but the type changes
        - Recurse if the key exists in both, the types are the same, and the
            value to update with is a dict
    """

    if isinstance(src, dict):
        for k, v in src.items():
            if k not in dst:
                dst[k] = v
            else:
                if isinstance(dst[k], dict) and isinstance(v, dict):
                    recursive_dict_update(dst[k], v)
                else:
                    dst.update(src)

def add_field_value(target, start_len, value):
    
    if target is None:
        target = []

    while len(target) != start_len:
        target.append(None)

    target.append(value)

    return target

class jsonDb(BaseBinDb):
    """ This is a JSON implementation of the BaseBinDB base class.

    See app.database.BaseBinDb (in __init__.py) for public API information
    """

    def __init__(self, path='database.json', time_format='%Y-%m-%d %H:%M:%S'):

        self._path = path

        self._key_bins = 'bins'
        self._key_sensors = 'sensors'
        self._key_data = 'data'
        self._key_data_timestamps = 'timestamps'    # Key for recording timestamps
        self._key_data_recorded_by = 'recorded_by'
        self._key_linked_to = 'bin_number'

        self._time_format = time_format

        if os.path.exists(self._path):
            try:
                with open(self._path, 'r') as fd:
                    data = json.load(fd)
            except Exception:
                print("unable to load existing data")
                fd = open(self._path, 'w')
                json.dump(self._base_structure(), fd)
                fd.close()
        else:
            fd = open(self._path, 'w')
            json.dump(self._base_structure(), fd)
            fd.close()

    def _base_structure(self):

        _base = dict()
        _base[self._key_bins] = dict()
        _base[self._key_sensors] = dict()
        _base[self._key_data] = dict()

        return _base

    def _update(self, update_with):
        data = self.data

        recursive_dict_update(data, update_with)

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
        else:
            bin_obj["lat"] = None
            bin_obj["long"] = None

        bin_obj["capacity"] = capacity

        if fill_threshold is not None:
            bin_obj["threshold"] = fill_threshold
        elif fill_threshold is None and capacity is not None:
            bin_obj["threshold"] = capacity
        else:
            bin_obj["threshold"] = None

        self._update({self._key_bins: {bin_id: bin_obj}})
    
    def add_sensor(self, sensor_id, sensor_type=None, linked_to=None):
        
        sens_obj = dict()

        sens_obj["type"] = sensor_type

        if self.is_bin(linked_to):
            sens_obj[self._key_linked_to ] = linked_to
        else:
            sens_obj[self._key_linked_to ] = None

        self._update({self._key_sensors: {sensor_id: sens_obj}})

    def add_data(self, sensor_id, value, field='values', timestamp=None):
        
        if not(self.is_sensor(sensor_id)):
            return None
        
        linked_bin = self.get_info_sensor(sensor_id, key=self._key_linked_to)
        if linked_bin is None:
            return None

        if timestamp is None:
            timestamp = datetime.now()
        
        timestamp_as_str = timestamp.strftime(self._time_format)

        # If no entries exist for this bin, make the base structure
        if self.get_data_bin(linked_bin) is None:
            _record_obj = dict()
            _record_obj[self._key_data_timestamps] = [timestamp_as_str]
            _record_obj[field] = [value]
            _record_obj[self._key_data_recorded_by] = [sensor_id]

            _data_obj = {self._key_data: {linked_bin: _record_obj}}

        else:
            _existing_record = self.get_data_bin(linked_bin)

            # The timestamp key is the only key that is gauranteed to be written
            # We need to make sure that new fields are padded
            n_existing_records = len(_existing_record[self._key_data_timestamps])

            _add = {field: value, self._key_data_recorded_by:sensor_id}

            for f, v in _add.items():
                if (f not in _existing_record):
                    _existing_record[f] = add_field_value(None, n_existing_records, v)
                elif (len(_existing_record[f]) < n_existing_records):
                    _existing_record[f] = add_field_value(_existing_record[f], n_existing_records, v)
                else:
                    _existing_record[f].append(v)

            _data_obj = {self._key_data: {linked_bin: _existing_record}}

            _existing_record[self._key_data_timestamps].append(timestamp_as_str)

        self._update(_data_obj)

    def add_diagnostics(self, sensor_id, value, field='diagnostics', timestamp=None):

        if not(self.is_sensor(sensor_id)):
            return None
        
        if timestamp is None:
            timestamp = datetime.now()
        
        timestamp_as_str = timestamp.strftime(self._time_format)

        # If no entries exist for this bin, make the base structure
        if self.get_data_sensor(sensor_id) is None:
            _record_obj = dict()
            _record_obj[self._key_data_timestamps] = [timestamp_as_str]
            _record_obj[field] = [value]

            _data_obj = {self._key_data: {self._key_sensors: {sensor_id: _record_obj}}}

            self._update(_data_obj)
        else:
            _existing_record = self.get_data_sensor(sensor_id)
            _existing_record[self._key_data_timestamps].append(timestamp_as_str)
            _existing_record[field].append(value)

            _data_obj = {self._key_data: {self._key_sensors: {sensor_id: _existing_record}}}

            self._update(_data_obj)

    def get_data_bin(self, bin_id, starting=None, ending=None):
        
        try:
            return self.data[self._key_data][bin_id]
        except KeyError:
            return None

    def get_data_sensor(self, sensor_id, starting=None, ending=None):

        try:
            return self.data[self._key_data][self._key_sensors][sensor_id]
        except KeyError:
            return None

    def get_info_bin(self, bin_id, key=None):
        """ Returns the bin information for a particular bin
        """

        if not(self.is_bin(bin_id)):
            return None
        else:
            if key == None:
                return self.data[self._key_bins][bin_id]
            else:
                if key not in self.data[self._key_bins][bin_id]:
                    return None
                else:
                    return self.data[self._key_bins][bin_id][key]

    def get_info_sensor(self, sensor_id, key=None):

        if not(self.is_sensor(sensor_id)):
            return None
        else:
            if key == None:
                return self.data[self._key_sensors][sensor_id]
            else:
                if key not in self.data[self._key_sensors][sensor_id]:
                    return None
                else:
                    return self.data[self._key_sensors][sensor_id][key]

    def get_all_bins(self):

        if self.data[self._key_bins] is None:
            return []
        else:
            return [x for x in self.data[self._key_bins]]
    
    def get_all_sensors(self):
        
        if self.data[self._key_sensors] is None:
            return []
        else:
            return [x for x in self.data[self._key_sensors]]

    def is_bin(self, test_id):
        
        if test_id in self.get_all_bins():
            return True
        else:
            return False

    def is_sensor(self, test_id):
        
        if test_id in self.get_all_sensors():
            return True
        else:
            return False
Documentation
=============

BaseBinDb
---------

This is an abstract base class that all implementations should
derive from

.. autoclass:: trashyApp.database.BaseBinDb
   :members: data, add_bin, get_info_bin

JsonDb
------

.. autoclass:: trashyApp.database.jsonDb
   :members: _base_structure, _update, data, add_bin, add_sensor, add_data, add_diagnostics, get_data_bin, get_data_sensor, get_info_bin, get_info_sensor, get_all_bins, get_all_sensors, is_bin, is_sensor
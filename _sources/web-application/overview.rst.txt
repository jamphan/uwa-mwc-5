.. _web-application-overview:

Web Application
===============

The dashboard application is built using a combination of Python Flask and mqtt-flask.

Quickstart
----------

You will need to install the ``trashyApp`` package using pip

.. code-block:: bash

   $ cd /path/to/Repo/                      # TLD
   $ python -m pip install -e ./trashyApp/

.. note::
   
   Again, we are using the ``-e`` switch with ``pip`` as the package is still
   under development

Once the package is installed, you should be able to run the package anywhere ``python``
is callable.

.. code-block:: bash

   $ python -m trashyApp

By default, this will run an Flask instance on ``http://127.0.0.1:5000/``

Configuration
-------------

Configuration of the application is done through two files:

- A ``.ini`` file that follows a certain format
- The ``trashyApp.conf`` module (``trashyApp/conf.py``)

A sample ``.ini`` file is shown below:

.. code-block:: ini

   [MQTT]
   broker_url = m2m.eclipse.org
   topics_subscribe = UWA/CITS/DATA;
   
   [DATABASE]
   type = json
   path =
   file = data.json
   
   [FLASK]
   server_name = 127.0.0.1:5000
   debug = True
 
All fields may be left blank as defaults specified in ``conf.py`` will be used.
In the ``conf.py`` file, you must specify the path to the config file of you choice

.. code-block:: python

   # conf.py
   # ...

   # Specifies the .ini file to use for configuration.
   # Use None for default configuration
   _CONFIG_FILE = None
   
   # Uncomment to use your own config file
   # _CONFIG_FILE_DIR = None
   # _CONFIG_FILE_NAME = None
   # _CONFIG_FILE = os.path.join(_CONFIG_FILE_DIR, _CONFIG_FILE_NAME
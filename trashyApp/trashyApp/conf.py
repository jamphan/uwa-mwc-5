""" Configure the Python Flask application
"""

import configparser
import os

# Specifies the .ini file to use for configuration.
# Use None for default configuration
_CONFIG_FILE = None
_CONFIG_TYPE_SELECT = ['Base', 'Production']
_CONFIG_TYPE = _CONFIG_TYPE_SELECT[0]

# Defaults
# These variables are only used when there are issues with loading
# the specified configuration, or if any critical variables are missing
_DEFAULT_CONFIG_FILE = 'conf.ini'
_DEFAULT_SERVER_NAME = '127.0.0.1:5000'
_DEFAULT_DATABASE_PATH = '.'

def get_config(path):

    if path is None:
        path = _DEFAULT_CONFIG_FILE

    conf = configparser.ConfigParser(allow_no_value=True)
    conf.optionxform = str
    conf.read(path)

    return conf

class Config(object):

    def __init__(self, path=None):

        self.conf = get_config(path)

        self.SERVER_NAME = self.conf['FLASK']['server_name']
        if self.SERVER_NAME == '':
            self.SERVER_NAME = _DEFAULT_SERVER_NAME
        
        self.DEBUG = bool(self.conf['FLASK']['debug'])

        # The type specifies what the interface class uses
        # This may either be 'JSON'
        self.DATABASE_TYPE = self.conf['DATABASE']['type']

        # Database path
        # If the database path is not specified, use the default
        # path (which is relative to the package)
        if self.conf['DATABASE']['path'] == '':
            self.conf['DATABASE']['path'] = _DEFAULT_DATABASE_PATH

        self.DATABASE_PATH = os.path.join(self.conf['DATABASE']['path'],
                                          self.conf['DATABASE']['file'])

        # Configure the MQTT client
        self.MQTT_BROKER_URL = self.conf['MQTT']['broker_url']

        # The MQTT topics are semi-comma delimited in the configuration file
        # we also remove the tail-end topic which is likely to be blank
        # TODO: Check the delimiter is correct
        self.MQTT_TOPICS = [x.strip() for x in self.conf['MQTT']['topics_subscribe'].split(';') if x.strip() != '']

class ProductionConfig(Config):

    def __init__(self):
        super(ProductionConfig, self).__init__(self)

        # Overwrite the base settings
        self.DEBUG = False
        self.TESTING = False

if _CONFIG_TYPE == 'Base':
    AppConfig = Config(path=_CONFIG_FILE)
elif _CONFIG_TYPE == 'Production':
    AppConfig = ProductionConfig(path=_CONFIG_FILE)
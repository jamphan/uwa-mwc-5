import re
from flask import Flask, render_template
from flask_mqtt import Mqtt

from app.database.jsonDb import jsonDb

# Constants
DB_PATH = 'uwa_bins.db'
MQTT_BROKER_HOST =  'm2m.eclipse.org'
MQTT_TOPICS = ['UWA/CITS/#']

class BinServer(object):
    """ Subscribes to the relevant MQTT messages and displays onto Flask App
    """

    def __init__(self, db_path='uwa_bins.db', db_type='json'):

        self._flask = Flask(__name__)
        self._flask.config['MQTT_BROKER_URL'] = MQTT_BROKER_HOST
        self._db_path = db_path

        if db_type == 'json':
            self._db = jsonDb(path=db_path)

        self._mqtt = Mqtt(self._flask)
        for topic in MQTT_TOPICS:
            self._mqtt.subscribe(topic)

    def flask_route(self, func):

        def wrapper_flaskroute():
        
                func(self._db)
        
        return wrapper_flaskroute

    def flask_run(self, debug=False):
        self._flask.run_server(debug=debug)

    @property
    def on_mqtt(self):
        return self._mqtt.on_message()

""" Main routines for Python Flask app.
"""

import os
import re
from flask import Flask, render_template
from flask_mqtt import Mqtt

from .database import get_db

# The application config is taken from this object. The object itself is a 
# class instantiated in the .conf.py module; there are various variants 
# derviced from a bass class. To selec the configuration to use, modify
# this config file
from .conf import AppConfig

def configure_apps():
    """ Returns the configured Python Flask application object

    Returns:
        flask.Flask: configured python flask object
        mqtt.Mqtt: configured MQTT flask app
    """

    # create and configure the app
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(AppConfig)

    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    mqtt = Mqtt()
    mqtt.init_app(flask_app)
    
    for topic in AppConfig.MQTT_TOPICS:
        mqtt.subscribe(topic)

    return flask_app, mqtt

def main():

    flaskApp, mqttApp = configure_apps()

    @mqttApp.on_message()
    def _(client, userdat, message):

        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )

        print(data.payload)
        incoming = data.payload
        parts = incoming.split(',')

        sensor_id = parts[0]
        bin_val = float(parts[1])

        with flaskApp.app_context():
            try:
                db = get_db()
                db.add_data(sensor_id, bin_val, field="values")
            except Exception as e:
                print(e)

    @flaskApp.route('/')
    def index():

        db = get_db()
        bin_ids = db.get_all_bins()
        print(bin_ids)
        data = db.data

        return render_template('home.html', data=data, bin_ids = bin_ids)

    @flaskApp.route('/datalog')
    def datalog():
        db = get_db()

        bin_ids = db.get_all_bins()
        sensor_ids = db.get_all_sensors()

        sensorData = db.data["sensors"];
        binData = db.data["bins"];

        database = db.data["data"]

        return render_template('datalog.html',
                               bin_data=binData,
                               bin_ids=bin_ids, 
                               sensor_ids = sensor_ids, 
                               sensor_data = sensorData,
                               data = database)

    @flaskApp.route('/settings')
    def settings():
        db = get_db()
        bin_ids = db.get_all_bins()
        return render_template('settings.html',  bin_ids = bin_ids)

    @flaskApp.route('/sensors')
    def sensors():
        db = get_db()
        bin_ids = db.get_all_bins()

        # create bin id array
        options = []
        options.append({"text":"All Bins", "value": "All bins"})
        for ids in bin_ids:
            options.append({"text": "Bin "+ re.search(r'\d+', ids).group(), "value": ids})
        
        return render_template('sensors.html', data=db.data, bin_ids = bin_ids, options = options)

    flaskApp.run()
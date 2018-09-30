import os
import re
from flask import Flask, render_template
from flask_mqtt import Mqtt

MQTT_BROKER = "m2m.eclipse.org"
MQTT_TOPIC = "UWA/CITS/DATA"

from .database import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data.json'),
        MQTT_BROKER_URL = MQTT_BROKER
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app

def mqtt_app(flask_app):

    mqtt = Mqtt()
    mqtt.init_app(flask_app)

    mqtt.subscribe(MQTT_TOPIC)

    return mqtt

def main():

    flaskApp = create_app()
    mqttApp = mqtt_app(flaskApp)

    @mqttApp.on_message()
    def _(client, userdat, message):

        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )

        print(message.payload.decode())
        incoming = message.payload.decode()
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

        return render_template('datalog.html',  bin_data=binData, bin_ids=bin_ids, 
                                                sensor_ids = sensor_ids, 
                                                sensor_data = sensorData, data = database)
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

    flaskApp.run(host='127.0.0.1', port=5000, debug=True)

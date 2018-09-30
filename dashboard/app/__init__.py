import os
import re
from flask import Flask, render_template
from flask_mqtt import Mqtt

from app.database import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data.json'),
        MQTT_BROKER_URL = 'm2m.eclipse.org'
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

flaskApp = create_app()

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

if __name__ == '__main__':
	flaskApp.run_server(debug=True)

import re
from flask import Flask, render_template
from flask_mqtt import Mqtt

from app.database.jsonDb import jsonDb

DATABASE_PATH = 'data.json'

flaskApp = Flask(__name__)
flaskApp.config['MQTT_BROKER_URL'] = 'm2m.eclipse.org'

@flaskApp.route('/')
def index():

    db = jsonDb(DATABASE_PATH)
    bin_ids = db.get_all_bins()
    print(bin_ids)
    data = db.data

    return render_template('home.html', data=data, bin_ids = bin_ids)

@flaskApp.route('/datalog')
def datalog():
    db = jsonDb(DATABASE_PATH)

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
    db = jsonDb(DATABASE_PATH)
    bin_ids = db.get_all_bins()
    return render_template('settings.html',  bin_ids = bin_ids)

@flaskApp.route('/sensors')
def sensors():
    db = jsonDb(DATABASE_PATH)
    bin_ids = db.get_all_bins()

    # create bin id array
    options = []
    options.append({"text":"All Bins", "value": "All bins"})
    for ids in bin_ids:
        options.append({"text": "Bin "+ re.search(r'\d+', ids).group(), "value": ids})
    
    return render_template('sensors.html', data=db.data, bin_ids = bin_ids, options = options)

if __name__ == '__main__':
	flaskApp.run_server(debug=True)

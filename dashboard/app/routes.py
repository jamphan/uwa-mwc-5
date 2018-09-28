from app import server
from flask import render_template
from app import flaskApp
from app.database.jsonDb import jsonDb

@flaskApp.route('/')
@flaskApp.route('/index')
@flaskApp.route('/dash')
def index():

    db = jsonDb('app/data.json')
    bin_ids = db.get_all_bins()
    print(bin_ids)
    data = db.data

    return render_template('home.html', data=data, bin_ids = bin_ids)

@flaskApp.route('/datalog')
def datalog():
    db = jsonDb('app/data.json')

    bin_ids = db.get_all_bins()
    sensor_ids = db.get_all_sensors()

    sensorData = db.data["sensors"];
    binData = db.data["bins"];

    database = db.data["data"]

    return render_template('datalog.html',  bin_data=binData, bin_ids=bin_ids, 
                                            sensor_ids = sensor_ids, 
                                            sensor_data = sensorData, data = database)

@flaskApp.route('/sensors')
def sensors():
    db = jsonDb('app/data.json')
    bin_ids = db.get_all_bins()

    # create bin id array
    options = []
    options.append({"text":"All Bins", "value": "All bins"})
    for ids in bin_ids:
        options.append({"text": "Bin "+ ids[3], "value": ids})
    
    # create graph dataset array, time, rssi
    # dataset = []
    # for ids in bin_ids:
        # binDataList = []
        # binData = db.data["data"][ids]
        # numReadings = len(binData)
        # for x in range(numReadings):
        #     rssi = binData["RSSI_values"][x]
        #     time = binData["timestamps"][x]
        #     binDataList.append([rssi, time])
        # dataset.append(binDataList);
    # print(dataset)
    return render_template('sensors.html', data=db.data, bin_ids = bin_ids, options = options)
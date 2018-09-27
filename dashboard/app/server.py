import json

def getJSON():
    with open("app/sensorData.json") as f:
        data = json.load(f)
        print(data["sensors"][0]);
    return(data)  
import json, os, io

def getJSON():
    with open("app/data.json") as f:
        data = json.load(f)
    return(data)  

def addToJSON(data):
    if os.path.exists("./data.json"):
        # checks if file exists
        print ("./data.json File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")
        with open(os.path.join("./", "data.json"), 'w') as db_file:
            db_file.write("hi")
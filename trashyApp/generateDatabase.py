import sys, json, random
from datetime import datetime, timedelta
    
def random_level(current_level, threshold):

    per_full = current_level / threshold
    if per_full == 0:
        return threshold*(0.1-0.01)*random.random() + threshold*0.01
    elif per_full < 0.3:
        multiplier = rand_between(1, 1.9)
        return current_level*multiplier
    elif per_full < 0.6:
         multiplier = rand_between(1, 1.5)
         return current_level*multiplier
    elif per_full < 0.8:
         multiplier = rand_between(1, 1.2)
         return current_level*multiplier
    multiplier = rand_between(1, 1.05)
    return current_level*multiplier
        

def rand_between(start, stop):
    return abs((stop-start)*random.random() + start)


jsonFile = open("data.json", "r") # Open the JSON file for reading
data = json.load(jsonFile) # Read the JSON into the buffer
jsonFile.close() # Close the JSON file

## Working with buffered content
bin_ids = []
for key in data["bins"]:
    bin_ids.append(key)

print(bin_ids)

for bin in bin_ids:
    print(data["data"][bin])
    data["data"][bin]["timestamps"] = []
    data["data"][bin]["RSSI_values"] = []
    data["data"][bin]["values"] = []

start_date = datetime(2018,9,25)
end_date = datetime.now()
step = timedelta(hours=1)
current_date = start_date

lowestR = 30
highR = 150
threshold = 100
while current_date < end_date:
    for bin in bin_ids:
        if current_date  == start_date:
            data["data"][bin]["values"].append(random.randint(30,150))
            data["data"][bin]["RSSI_values"].append(random.randint(80,120))
        
        else:
            newRSSI = (data["data"][bin]["RSSI_values"][-1]*10 + random.randint(80,120))/11
            data["data"][bin]["RSSI_values"].append(newRSSI)

            newValue = data["data"][bin]["values"][-1] + 16*random.randint(0,100)/100

            if newValue >= 120:
                newValue = 0

            data["data"][bin]["values"].append(newValue)

            # if newValue >= 150:
            #     newValue = 0

        data["data"][bin]["timestamps"].append(current_date.strftime('%Y-%m-%d %H:%M'))
    current_date = current_date + step

## Save our changes to JSON file
jsonFile = open("data.json", "w+")
jsonFile.write(json.dumps(data))
jsonFile.close()


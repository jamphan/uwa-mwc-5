$(document).ready(function () {

    var table = $('#myTable').DataTable({
        "bProcessing": true,
    });
    
    num_bins = bin_ids.length;
    for(var i = 0; i < num_bins; i++){
        num_records = data[bin_ids[i]]["timestamps"].length;
        for(var j = 0; j < 1; j++){
            var binID = bin_ids[i];
            var bin = data[binID];
            var time = bin["timestamps"][j];
            var value = bin["values"][j];
            var RSSI = bin["RSSI_values"][j];
            var sensorID = bin_data[binID]["sensorid"];
            var long = bin_data[binID]["lat"];
            var lat = bin_data[binID]["long"];

            var sensorType = sensor_data[sensorID]["type"];
            table.row.add(
                [time, binID, sensorID, value, lat, long, RSSI, sensorType]
            ).draw();
        }
    }
});
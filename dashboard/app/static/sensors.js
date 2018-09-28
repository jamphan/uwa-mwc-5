$(document).ready(function () {    
    var $select = $('#input-tags').selectize({
        delimiter: ',',
        create: false,
        persist: false,
        options: options,
        closeAfterSelect: true,
        valueField: 'text',
        items: ["Bin 1"],
        plugins: ['remove_button', 'drag_drop'],
        create: function(input) {
            return {
                value: input,
                text: input
            }
        }
    });

    $select[0].selectize.$control_input.on('keydown', function(e) {
        var key = e.charCode || e.keyCode;
        if(key == 8 )
            return true;
        else
            e.preventDefault();
    });
    var rssi_chart = document.getElementById("rssi-chart").getContext('2d');
    var level_chart = document.getElementById("fill-level-chart").getContext('2d');
    refreshRSSIGraph($select[0].selectize.getValue(), rssi_chart);
    refreshLevelGraph($select[0].selectize.getValue(), level_chart);

    $select[0].selectize.on('change', function(value) {
        refreshRSSIGraph(value, rssi_chart);
        refreshLevelGraph(value, level_chart);
    });

});
function getBinData(){
    var Color = [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(143, 43, 96, 0.6)',
        
    ]
    var binData = [];
    for(var i = 0; i < bin_ids.length; i++){
        bin_label = bin_ids[i];
        dataset = [];
        for(var j = 0; j < data["data"][bin_label]["timestamps"].length; j++){
            dataset.push({x: new Date(data["data"][bin_label]["timestamps"][j]), y: data["data"][bin_label]["RSSI_values"][j]});
        }
        binData.push({label: bin_label, data: dataset, backgroundColor: Color[i], borderColor: Color[i], fill: false});
    }
    return binData;
}

function getLevelData(){
    var Color = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(143, 43, 96, 0.2)',
        
    ]
    var binData = [];
    for(var i = 0; i < bin_ids.length; i++){
        bin_label = bin_ids[i];
        dataset = [];
        for(var j = 0; j < data["data"][bin_label]["timestamps"].length; j++){
            const depth = data["bins"][bin_label]["depth"];
            const value = data["data"][bin_label]["values"][j];
            const thresh = data["bins"][bin_label]["threshold"];
            var percentFilled = (depth-value)/(depth-thresh)*100;
            dataset.push({x: new Date(data["data"][bin_label]["timestamps"][j]), y: percentFilled});
        }
        binData.push({label: bin_label, data: dataset, backgroundColor: Color[i], borderColor: Color[i], fill: true});
    }
    return binData;
}
function refreshRSSIGraph(selectList, rssi_chart){
    console.log(selectList);
    allbinData = getBinData();
    selectbinData = [];
    if(selectList.length == 0){
        console.log("none selected");
        selectbinData = allbinData;
    }
    else{
        selectList = selectList.split(',');
        for(var i = 0; i < selectList.length; i++){
            if(selectList.indexOf("All Bins") > -1){
                selectbinData = allbinData;
                break;
            }
            else{
                // var num = options.indexOf(selectList[i]);
                bin = selectList[i].replace(/\s+/g,'').toLowerCase();
                index = bin_ids.indexOf(bin);
                selectbinData.push(allbinData[index]);
            }
        }
    }

    console.log(selectList);
    var chart = new Chart(rssi_chart, {
        type: 'line',
        data: {
            datasets: selectbinData,
        },
        options: {
            events: [],
            scales: {
                xAxes: [
                  {
                    type: 'time',
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        labelString: "Time & Date",
                    },
                    time: {
                        displayFormats: {
                            quarter: 'MMM D h:mm a'
                        }
                    }
                  }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "RSSI",
                        }, 
                        ticks: {
                            reverse: true,
                        }
                    }
                ]
            }
        }
    });
}
function refreshLevelGraph(selectList, level_chart){
    console.log(selectList);
    allbinData = getLevelData();
    selectbinData = [];
    if(selectList.length == 0){
        console.log("none selected");
        selectbinData = allbinData;
    }
    else{
        selectList = selectList.split(',');
        for(var i = 0; i < selectList.length; i++){
            if(selectList.indexOf("All Bins") > -1){
                selectbinData = allbinData;
                break;
            }
            else{
                // var num = options.indexOf(selectList[i]);
                bin = selectList[i].replace(/\s+/g,'').toLowerCase();
                index = bin_ids.indexOf(bin);
                selectbinData.push(allbinData[index]);
            }
        }
    }

    console.log(selectList);
    var chart = new Chart(level_chart, {
        type: 'line',
        data: {
            datasets: selectbinData,
        },
        options: {
            events: [],
            scales: {
                xAxes: [
                  {
                    type: 'time',
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        labelString: "Time & Date",
                    },
                    time: {
                        displayFormats: {
                            quarter: 'MMM D h:mm a'
                        }
                    }
                  }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "RSSI",
                        }, 
                        ticks: {
                            reverse: false,
                        }
                    }
                ]
            }
        }
    });
}
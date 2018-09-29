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
    var rchart;
    var lchart;
    rchart = refreshRSSIGraph($select[0].selectize.getValue(), rssi_chart, rchart);
    lchart = refreshLevelGraph($select[0].selectize.getValue(), level_chart, lchart);
    $select[0].selectize.on('change', function(value) {
        rchart = refreshRSSIGraph(value, rssi_chart, rchart);
        lchart = refreshLevelGraph(value, level_chart, lchart);
    });

});

function clearChart(id){
    $('#' + id).empty();
    $('#' + id).html('<canvas id='+id +'width="50%" height="35%"></canvas>');
}
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

function refreshRSSIGraph(selectList, rssi_chart, rchart){
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
    if(rchart != undefined){
        rchart.destroy();
    }
    rchart = new Chart(rssi_chart, {
        type: 'line',
        data: {
            datasets: selectbinData,
        },
        options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                       var label = "RSSI";
                       return label + ' : ' + tooltipItem.yLabel;
                    }
                }
            },
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
    return rchart;
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

    if(lchart != undefined){
        lchart.destroy();
    }
    var lchart = new Chart(level_chart, {
        type: 'line',
        data: {
            datasets: selectbinData,
        },
        options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                       var label = "Fill (%)";
                       return label + ' : ' + tooltipItem.yLabel;
                    }
                }
            },
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
                        },
                        stepSize: 30
                    }
                  }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Fill (%)",
                        },
                        min: 0, 
                        ticks: {
                            reverse: false,
                        }
                    }
                ]
            }
        }
    });
    return lchart;
}
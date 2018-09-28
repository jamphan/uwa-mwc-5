$(document).ready(function () {
    processData();
});

function processData(){
    const table = document.getElementById('sensor-table');
    table.innerHTML = "";
    num_bins = bin_ids.length;
    for (var i = 0; i < num_bins; i++){
        const num = i + 1;

        const bin = data["bins"][bin_ids[i]];

        const depth = bin["depth"];
        const thresh = bin["threshold"];

        const binData = data["data"][bin_ids[i]];

        const dataLength = binData["values"].length;
        const lastValue = binData["values"][dataLength-1];

        var percentFilled = (depth-lastValue)/(depth-thresh)*100;
        var barColor = 'bg-info';
        var status = '<td><img class="bin-alert" width="18px" src = "/static/images/check.png"></td';;
        if(percentFilled < 0 || percentFilled > 100){
            status = '<td><img class="bin-alert" width="20px" src = "/static/images/wrench.png"></td';
            percentFilled = 0;
        }
        if(percentFilled > 60)
            barColor = 'bg-warning';
        if(percentFilled > 85){
            barColor = 'bg-danger';
             status = '<td><img class="bin-alert" width="20px" src = "/static/images/exclamation-mark.png"></td';
        }
        table.insertAdjacentHTML('beforeend', '<tr><td><b>'+num+'</b></td><td><div class="progress"><div class="progress-bar-striped progress-bar ' + barColor +'" role="progressbar" style="width: '+ percentFilled + '%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div></div></td><td>'+percentFilled+'%</td>'+status+'</tr>');
        // add bin marker to google map
        var marker = new google.maps.Marker({
            position: {lat: bin["lat"],lng: bin["long"]},
            map: map,
            title: bin_ids[i],
            label: {text: num.toString(), color: "white"},
        });
        google.maps.event.addListener(marker, "click", function (event) {
            alert(this.position);
        });
    }
};

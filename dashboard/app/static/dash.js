$(document).ready(function () {

    
    processData();

    $('#sidebarCollapse').on('click', function () {
        // open or close navbar
        $('#sidebar').toggleClass('active');
        // close dropdowns
        $('.collapse.in').toggleClass('in');
        // and also adjust aria-expanded attributes we use for the open/closed arrows
        // in our CSS
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        $(this).toggleClass('active');
        if($('#sidebar').hasClass('active')){
            $('.sidebar-label, .sidebar-title').toggleClass('hidden');
        }
        else{
            setTimeout(function() {
                $('.sidebar-label, .sidebar-title').toggleClass('hidden');
              }, 110);
        }
    });
});

function processData(){
    const table = document.getElementById('sensor-table');
    num_bins = bin_ids.length;
    for (var i = 0; i < num_bins; i++){
        const bin = data["bins"][bin_ids[i]];
        const depth = bin["depth"];
        const thresh = bin["threshold"];
        const binData = data["data"][bin_ids[i]];
        const dataLength = binData["values"].length;
        const lastValue = binData["values"][dataLength-1];
        const PercentFilled = (depth-lastValue)/(depth-thresh);
        table.insertAdjacentHTML('beforeend', '<tr><td><b>'+i+'</b></td><td>' + PercentFilled+ '</td></tr>');
        const num = i + 1;
        // add bin marker to google map
        var marker = new google.maps.Marker({
            position: {lat: bin["lat"],lng: bin["long"]},
            map: map,
            title: bin_ids[i],
            label: num.toString(),
        });
    }
};

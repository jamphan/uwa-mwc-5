$(document).ready(function () {

    
    makeSensorTable();
    var marker = new google.maps.Marker({
        position: {lat: -31.9787,lng: 115.8174},
        map: map,
        title: 'Hello World!',
        label: '1',
    });

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

function makeSensorTable(){
    const table = document.getElementById('sensor-table');
    console.log(Object.keys(data["bins"]).length);
    for(var i = 1; i <= Object.keys(data["bins"]).length; i++){
        const bin = data["bins"]["bin"+ i];
        const depth = bin["depth"];
        const thresh = bin["threshold"];
        const binData = data["data"]["bin" + i];
        const dataLength = binData.length;
        const lastValue = binData["values"][dataLength-1];
        table.insertAdjacentHTML('beforeend', '<tr><td><b>'+i+'</b></td><td>' + lastValue+ '</td></tr>');
    }
};

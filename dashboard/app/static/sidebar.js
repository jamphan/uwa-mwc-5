$(document).ready(function () {
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
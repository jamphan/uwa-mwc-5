$(document).ready(function () {    
    var $select = $('#sensor_select').selectize({
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
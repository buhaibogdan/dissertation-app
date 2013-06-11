$(document).ready(function(){
    $('#start_date').datepicker();
    $('#end_date').datepicker();

    $('#btn_filter').on("click", function(evt){
        evt.preventDefault();

        var data = {};
        data.startDate = $('#start_date').val();
        data.endDate = $('#end_date').val();
        data.type = $('#log_type').val();

        $.ajax({
            url: '/',
            type: 'GET',
            data: data,
            complete: function(xhr){

            }
        });
    });
})

/*|-------------------------|*/
/*|----Utility functions----|*/
/*|-------------------------|*/
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}


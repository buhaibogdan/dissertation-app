$(document).ready(function(){
    $('#report_generate').on('click', function(evt){
        evt.preventDefault()
        pid = $('#projects_list').val()
        $.ajax({
           url: '/reports',
           data: {'pid':pid},
           type: 'POST',
           complete: function(xhr){
               if (xhr.status == 200){
                   $('#report_failed').hide();
                   $('#report_send').show();
               } else {
                   $('#report_failed').show();
                   $('#report_send').hide();
               }
           }
        });
    });
})
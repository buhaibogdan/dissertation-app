$(document).ready(function(){
    Issues.init();
});

Issues = {} || Issues;
Issues.init = function(){
    $('.task').draggable({
        handle:'.task-title',
        helper:'clone',
        appendTo: 'body'
    });

    $('#tasks_in_progress').droppable({
        "activeClass": '',
        'hoverClass': "ui-state-hover",
        'accept':'.task',
        drop: function(event, ui){
            ui.draggable.appendTo(this)
        }
    });

    $('#projects_list').on('change', function(){
        window.location.href = '/project/' + $(this).find('option:selected').val() + '/issues'
    });

    $("#btn_add_dev").on('click', function(){
        $('#new-issue-type').val(1);
    });

    $("#btn_add_qa").on('click', function(){
        $('#new-issue-type').val(2);
    });

    $("#btn_add_bug").on('click', function(){
        $('#new-issue-type').val(3);
    });

    $('#issue_add_new').on('click', function(){
        var method = 'PUT';
        var url = '/project/'+ $('#project_id').val() + '/issues';
        var data = $('#issue_add_update').serialize();
        $.ajax({
            url: url,
            method: method,
            data: data,
            complete: function(xhr){
                if (xhr.status == 201){
                    window.location.href = url;
                } else {
                    $('#error_not_saved').show();
                }
            }
        });
    });
};


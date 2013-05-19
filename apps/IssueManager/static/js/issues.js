$(document).ready(function(){
    Issues.init();
    Issues.enableDraggable();
});

Issues = {} || Issues;
Issues.url = (function(){
    return '/project/'+ $('#project_id').val() + '/issues';
})(jQuery);

Issues.reload = function(){
    window.location.href = '/project/'+ $('#project_id').val() + '/issues';
}

Issues.init = function(){


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
        var method = 'POST';
        var url = '/project/'+ $('#project_id').val() + '/issues';
        var data = $('#issue_add_update').serialize();
        $.ajax({
            url: url,
            type: method,
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
    // deleting a task
    // _xsrf must be passed as param for secure cookie
    // must be in get for DELETE method
    $('#task_columns .task .remove-task').on('click', function(evt){
        evt.preventDefault()
        var taskId = $(this).closest('.task').attr('data-id');
        var url = '/issue/'+taskId + '?_xsrf='+getCookie("_xsrf");
        var c =confirm("Sure?");
        if (!c){
            return;
        }
        $.ajax({
            type: 'DELETE',
            url: url,
            complete: function(xhr){
                if (xhr.status == 200){
                    Issues.reload();
                } else {
                    $('#error_not_deleted').show();
                }
            }
        })
    });

    $('#task_columns .task .log-work').on('click', function(evt){
        evt.preventDefault();
        var taskId = $(this).closest('.task').attr('data-id');
        var url = '/issue/'+taskId+'/time';
        $.ajax({
            type:"GET",
            url:url,
            complete: function(xhr){
                $('#logWorkModal').html(xhr.responseText);
                $('#log_work_auto_adjust').on('change', function(){
                    if ( !$(this).prop('checked') ){
                        $('#log_work_adjust_by').prop('disabled', false);
                    } else {
                        $('#log_work_adjust_by').prop('disabled', true);
                    }
                });
                $('#issue_log').on('click', function(){
                    var url = '/issue/'+ $('#task_id_log').val();
                    var data = $('#issue_log_work').serialize();
                    $.ajax({
                        type: 'PUT',
                        data: data,
                        url: url,
                        complete: function(xhr){
                            if (xhr.status == 200){
                                Issues.reload();
                            } else {
                                $('#error_work_not_logged').css({'visibility':'visible'});
                            }
                        }
                    })
                });
            }
        })
    });

};

Issues.enableDraggable = function(){
    $('.task').draggable({
        handle:'.task-title',
        helper:'clone',
        appendTo: 'body'
    });

    $('#tasks_in_progress').droppable({
        "activeClass": '',
        'hoverClass': "hover-status-progress",
        'accept':'.task.task-to-do, .task.task-done',
        drop: function(event, ui){
            var task_id = $(ui.draggable).closest('.task').attr('data-id');
            ui.draggable.appendTo(this);
            $.ajax({
                url: '/issue/'+task_id,
                type: 'PUT',
                data: {'status':'2', 'pid':$('#project_id').val()},
                complete: function(xhr){
                    if (xhr.status == 200){
                        Issues.reload();
                    } else {
                        $('#error_not_deleted').show();
                    }
                }
            });
        }
    });

    $('#tasks_done').droppable({
        "activeClass": '',
        'hoverClass': "hover-status-done",
        'accept':'.task.task-in-progress',
        drop: function(event, ui){
            var task_id = $(ui.draggable).closest('.task').attr('data-id');
            console.log(task_id);
            ui.draggable.appendTo(this);
            $.ajax({
                url: '/issue/'+task_id,
                type: 'PUT',
                data: {'status':'3', 'pid':$('#project_id').val()},
                complete: function(xhr){
                    if (xhr.status == 200){
                        Issues.reload();
                    } else {
                        $('#error_not_deleted').show();
                    }
                }
            });
        }
    });

    $('#tasks_todo').droppable({
        "activeClass": '',
        'hoverClass': "hover-status-todo",
        'accept':'.task.task-in-progress',
        drop: function(event, ui){
            var task_id = $(ui.draggable).closest('.task').attr('data-id');
            console.log(task_id);
            ui.draggable.appendTo(this);
            $.ajax({
                url: '/issue/'+task_id,
                type: 'PUT',
                data: {'status':'1', 'pid':$('#project_id').val()},
                complete: function(xhr){
                    if (xhr.status == 200){
                        Issues.reload();
                    } else {
                        $('#error_not_deleted').show();
                    }
                }
            });
        }
    });
}
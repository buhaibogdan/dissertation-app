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
        "activeClass": 'ui-state-default',
        'hoverClass': "ui-state-hover",
        'accept':'.task',
        drop: function(event, ui){
            ui.draggable.appendTo(this)
        }
    });
}
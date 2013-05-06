Projects = {} || Projects;

Projects.init = function(){
    $('#project_release').datepicker({'dateFormat':'yy-mm-dd'});
    $('#project_new').on('click', function(ev){
        ev.preventDefault();
        Projects.hideInfo();
    });

    $('#project_new_cancel').on('click', function(ev){
        ev.preventDefault();
        Projects.showInfo();
    });

    $('#projects_list').on('change', function(){
        var pid = $(this).find("option:selected").val()
        var $loadingImg = $('#loading_gif');
        $loadingImg.css("visibility", "visible");
        $.ajax({
            url: "/project/"+pid,
            method: "GET",
            complete: function(xhr){
                var project = $.parseJSON(xhr.responseText)
                $('#project_info_title').html(project.title)
                $('#project_info_owner').html(project.owner)
                $('#project_info_description').html(project.description)
                $('#project_info_release_date').html(project.release_date)
                $('#project_info_people_involved').html(project.people)
                $loadingImg.css("visibility", "hidden");
            }
        });
    });
    $('#project_edit').on('click', function(){
        var pid = $("#projects_list option:selected").val()
        var $loadingImg = $('#loading_gif');
        $loadingImg.css("visibility", "visible");
        $.ajax({
            url: "/project/"+pid,
            method: "GET",
            complete: function(xhr){
                Projects.hideInfo();
                var project = $.parseJSON(xhr.responseText);
                Projects.setValues(project);
                $loadingImg.css("visibility", "hidden");
            }

        });
    });

    $('#project_save').on('click', function(){
        var method = 'PUT';
        var url = '/projects';
        var data = $('#project_new_edit_form').serialize();
        $.ajax({
            url: url,
            method: method,
            data: data,
            complete: function(xhr){
                if (xhr.status == 201){
                    window.location.href = '/projects';
                } else {
                    $('#error_not_saved').show();
                }
            }
        });
    });
}


Projects.clearFields = function(){
    $("#project_title").val('')
    $("#project_description").val('')
    $("#project_release").val('');
    $("#project_send_email").prop('checked', false);
    $("#project_owner").val(0);
    $("#project_id").val('');
}

Projects.setValues = function(project){
    try{
        $("#project_id").val(project.pid);
        $("#project_title").val(project.title)
        $("#project_description").val(project.description)
        $("#project_release").val(project.release_date);
        $("#project_send_email").prop('checked', false);
        $("#project_owner").val(project.id_owner);
    } catch(e){
        console.log("Could not populate projects fields");
    }
}

Projects.hideInfo = function(){
    Projects.clearFields();
    $('#project_new_form').show();
    $('#project_info').hide();
    $('#projects_list').attr("disabled", "disabled");
    $('#error_not_saved').hide();
}

Projects.showInfo = function(){
    $('#project_new_form').hide();
    $('#project_info').show();
    $('#projects_list').removeAttr("disabled");
    $('#error_not_saved').hide();
}


$(document).ready(function(){
    Projects.init()
});
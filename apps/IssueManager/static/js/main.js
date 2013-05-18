$(document).ready(function(){
    WS.getAllHistory();
    WS.getMyHistory();

    var pid;
    if ( pid = $("#projects_list").val() ){
        WS.getProjectHistory(pid);
    }
})



/*|-------------------|*/
/*|-----Websockets----|*/
/*|-------------------|*/
WS = {} || WS;

WS.host  = 'ws://localhost:8000/history';

WS.init = function(){

};

WS.myHistoryWS = null;
WS.allHistoryWS = null;
WS.projectHistoryWS = null;
WS.userHistoryWS = null;

WS.getAllHistory = function(){
    if ( !$('#all_activity_list').length ){
        return false;
    }

    WS.allHistoryWS = new WebSocket(WS.host);
    WS.allHistoryWS.onopen = function (evt) {
        var intervalIDProject = setInterval(function(){
            WS.allHistoryWS.send('refresh');
            $('#loading_activity_all').toggleClass('invisible');
        }, 15000);
    };
    WS.allHistoryWS.onmessage = function(evt) {
        $('#loading_activity_all').toggleClass('invisible');
        var events = $.parseJSON(evt.data);
        WS.displayHTML('all_activity_list', events);

    };
    WS.allHistoryWS.onerror = function (evt) {
        console.log('error on all history');
        console.log(evt);
    };

    return true;
};

WS.getMyHistory = function(){
    if ( !$('#my_activity_list').length ){
        return false;
    }
    WS.myHistoryWS = new WebSocket(WS.host + '/user/' + $('#my_uid').val());
    WS.myHistoryWS.onopen = function (evt) {
        var intervalIDProject = setInterval(function(){
            WS.myHistoryWS.send('refresh');
            $('#loading_activity_my').toggleClass('invisible');
        }, 15000);
        console.log('websocket open to '+WS.host + '/user/' + $('#my_uid').val());
    };
    WS.myHistoryWS.onmessage = function(evt) {
        $('#loading_activity_my').toggleClass('invisible');
        var events = $.parseJSON(evt.data);
        WS.displayHTML('my_activity_list', events);
    };
    WS.myHistoryWS.onerror = function (evt) {
        console.log('error on my history');
        console.log(evt);
    };
    return true;
};

WS.getProjectHistory = function(pid){
    if ( !$('#project_activity_list').length ){
        return false;
    }
    WS.projectHistoryWS = new WebSocket(WS.host + '/project/' + pid);
    WS.projectHistoryWS.onopen = function (evt) {
        var intervalIDProject = setInterval(function(){
            WS.projectHistoryWS.send('refresh');
            $('#loading_activity_project').toggleClass('invisible');
        }, 15000);
    };
    WS.projectHistoryWS.onmessage = function(evt) {
        $('#loading_activity_project').toggleClass('invisible');
        var events = $.parseJSON(evt.data);
        WS.displayHTML('project_activity_list', events);

    };
    WS.projectHistoryWS.onerror = function (evt) {
        console.log('error on projectHistory');
        console.log(evt);
    };
    return true;
};

WS.getUserHistory = function(uid){
    if ( !$('#user_activity_list').length ){
        return false;
    }
    WS.userHistoryWS = new WebSocket(WS.host + '/user/'+ uid);
    WS.userHistoryWS.onopen = function (evt) {
        console.log('websocket open to '+ WS.host + '/user/'+ uid);
    };
    WS.userHistoryWS.onmessage = function(evt) {
        var events = $.parseJSON(evt.data);
        console.log(events);

    };
    WS.userHistoryWS.onerror = function (evt) {
        console.log('error on user history');
        console.log(evt);
    };
    return true;
};

WS.displayHTML = function(elemId, events){
    var nrEvents = events.length;
    for (var i=0;i<nrEvents;i++){
        var ev = events[i];
        $('<li />').html(ev.message).prependTo('#'+elemId);
    }
}

/*|-------------------|*/
/*|----/Websockets----|*/
/*|-------------------|*/


/*|-------------------------|*/
/*|----Utility functions----|*/
/*|-------------------------|*/
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}


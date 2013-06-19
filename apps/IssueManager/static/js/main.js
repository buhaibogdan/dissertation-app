$(document).ready(function(){
    WS.getAllHistory();
    WS.getMyHistory();

    var pid = $("#projects_list").val();
    if ( pid != 0 ){
        WS.getProjectHistory(pid);
    } else {
        WS.getProjectHistory(1);
    }
})



/*|-------------------|*/
/*|-----Websockets----|*/
/*|-------------------|*/
WS = {} || WS;

WS.host  = 'wss://localhost:8000/history';

WS.init = function(){

};

WS.myHistoryWS = null;
WS.allHistoryWS = null;
WS.projectHistoryWS = null;
WS.userHistoryWS = null;
WS.myHistoryIntervalId = null;
WS.allHistoryIntervalId = null;
WS.projectHistoryIntervalId = null;
WS.userHistoryIntervalId = null;

WS.getAllHistory = function(){
    if ( !$('#all_activity_list').length ){
        return false;
    }
    if ( WS.allHistoryWS != null){
        WS.allHistoryWS.close();
        clearInterval(WS.allHistoryIntervalId);
        WS.allHistoryWS = null;
    }
    WS.allHistoryWS = new WebSocket(WS.host);
    WS.allHistoryWS.onopen = function (evt) {
        WS.allHistoryIntervalId = setInterval(function(){
            WS.allHistoryWS.send('refresh');
            $('#loading_activity_all').removeClass('invisible');
        }, 15000);
    };
    WS.allHistoryWS.onmessage = function(evt) {
        var events = $.parseJSON(evt.data);
        WS.displayHTML('all_activity_list', events);
        $('#loading_activity_all').addClass('invisible');

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
    if ( WS.myHistoryWS != null){
        WS.myHistoryWS.close();
        clearInterval(WS.myHistoryIntervalId);
        WS.myHistoryWS = null;
    }
    WS.myHistoryWS = new WebSocket(WS.host + '/user/' + $('#my_uid').val());
    WS.myHistoryWS.onopen = function (evt) {
        $('#project_activity_list').empty();
        WS.myHistoryIntervalId = setInterval(function(){
            WS.myHistoryWS.send('refresh');
            $('#loading_activity_my').removeClass('invisible');
        }, 15000);
        console.log('websocket open to '+WS.host + '/user/' + $('#my_uid').val());
    };
    WS.myHistoryWS.onmessage = function(evt) {
        var events = $.parseJSON(evt.data);
        WS.displayHTML('my_activity_list', events);
        $('#loading_activity_my').addClass('invisible');
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
    if ( WS.projectHistoryWS != null){
        console.log('interval: ' + WS.projectHistoryIntervalId);
        WS.projectHistoryWS.close();
        clearInterval(WS.projectHistoryIntervalId);
        WS.projectHistoryWS = null;
    }
    WS.projectHistoryWS = new WebSocket(WS.host + '/project/' + pid);
    WS.projectHistoryWS.onopen = function (evt) {
        $('#project_activity_list').empty();
        WS.projectHistoryIntervalId = setInterval(function(){
            WS.projectHistoryWS.send('refresh');
            console.log('should be 15 secs');
            $('#loading_activity_project').removeClass('invisible');
        }, 15000);
    };
    WS.projectHistoryWS.onmessage = function(evt) {
        var events = $.parseJSON(evt.data);
        WS.displayHTML('project_activity_list', events);
        $('#loading_activity_project').addClass('invisible');

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
    var intervalIDProject;
    if ( WS.userHistoryWS != null){
        WS.userHistoryWS.close();
        clearInterval(WS.userHistoryIntervalId);
        WS.userHistoryWS = null;
    }
    WS.userHistoryWS = new WebSocket(WS.host + '/user/'+ uid);
    WS.userHistoryWS.onopen = function (evt) {
        $('#project_activity_list').empty();
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
    if (events.error){
        $('<li />').html('An error occurred while retrieving these events.').prependTo('#'+elemId);
    }

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


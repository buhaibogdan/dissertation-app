$(document).ready(function(){
    //WS.getAllHistory();
    WS.getMyHistory();
    WS.getUserHistory(3)
    WS.getProjectHistory(2)
})

function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}


WS = {} || WS;

WS.host  = 'ws://localhost:8000/history';

WS.init = function(){

};

WS.getAllHistory = function(){
    var websocket = new WebSocket(WS.host);
    websocket.onopen = function (evt) {
        console.log('websocket open to '+WS.host);
    };
    websocket.onmessage = function(evt) {
        events = $.parseJSON(evt.data);
        console.log(events);

    };
    websocket.onerror = function (evt) {
        console.log('error on all history');
        console.log(evt);
    };
};

WS.getMyHistory = function(){
    var websocket = new WebSocket(WS.host + '/user/' + $('#my_uid').val());
    websocket.onopen = function (evt) {
        console.log('websocket open to '+WS.host + '/user/' + $('#my_uid').val());
    };
    websocket.onmessage = function(evt) {
        events = $.parseJSON(evt.data);
        console.log(events);

    };
    websocket.onerror = function (evt) {
        console.log('error on my history');
        console.log(evt);
    };
};

WS.getProjectHistory = function(pid){
    var websocket = new WebSocket(WS.host + '/project/' + pid);
    websocket.onopen = function (evt) {
        console.log('websocket open to '+WS.host + '/project/' + pid);
    };
    websocket.onmessage = function(evt) {
        events = $.parseJSON(evt.data);
        console.log(events);

    };
    websocket.onerror = function (evt) {
        console.log('error on projectHistory');
        console.log(evt);
    };
};

WS.getUserHistory = function(uid){
    var websocket = new WebSocket(WS.host + '/user/'+ uid);
    websocket.onopen = function (evt) {
        console.log('websocket open to '+ WS.host + '/user/'+ uid);
    };
    websocket.onmessage = function(evt) {
        events = $.parseJSON(evt.data);
        console.log(events);

    };
    websocket.onerror = function (evt) {
        console.log('error on user history');
        console.log(evt);
    };
};

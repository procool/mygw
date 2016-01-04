var wS;
function start_chat_ws(host, port, params) {
    var wsaddr = "ws://" + host;
    if (port) wsaddr +=":" + port;
    wsaddr += "/messages/";

    var ws = new WebSocket(wsaddr);
    wS = ws;

    ws.onmessage = function(event) {
        var mdata = JSON.parse(event.data);
        console.log(event.data);
        if (mdata.owner == 'mygwcontrold') 
            ws_mygwcontrold_processor(mdata);
    }

    ws.onopen = function(){
        if (params && params.onsuccess)
            params.onsuccess(ws);
    }

    ws.onclose = function(){
        // Try to reconnect in 5 seconds
        setTimeout(function() {start_chat_ws(host, port)}, 5000);
    };

    return ws;

}

            
function ws_mygwcontrold_processor(mdata) {
    if (mdata.ident == 'plugin_uptime') {
        $(".js-admin-status-uptime").html(mdata.uptime);
        $(".js-admin-status-avg").html(mdata.load_average['0'] + ', ' + mdata.load_average['1'] + ', ' + mdata.load_average['2']);
    } else if (mdata.ident == 'plugin_messages') {
        $(".js-admin-status-messages").append('<div style="clear: both; padding-top: 3px;"><code>' + mdata.line + '</code></div>');
        $(".js-admin-status-messages-wrap").scrollTop($(".js-admin-status-messages-wrap").get(0).scrollHeight);

    } else {
        //orderslist_update_core.refresh();
    }
}


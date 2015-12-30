var statusd_wsocket;
function start_chat_ws(host, port) {
    var wsaddr = "ws://" + host;
    if (port) wsaddr +=":" + port;
    wsaddr += "/messages/";

    var ws = new WebSocket(wsaddr);
    statusd_wsocket = ws;

    ws.onmessage = function(event) {
        var mdata = JSON.parse(event.data);
        console.log(event.data);
        if (mdata.owner == 'ordersd') 
            ws_ordersd_processor(mdata);
        else if (mdata.owner == 'unitsd') 
            ws_unitsd_processor(mdata);
        else if (mdata.owner == 'webapibackend') 
            ws_webapibackend_processor(mdata);
    }

    ws.onopen = function(){
    }

    ws.onclose = function(){
        // Try to reconnect in 5 seconds
        setTimeout(function() {start_chat_ws(host, port)}, 5000);
    };

}

            
function ws_ordersd_processor(mdata) {
    if (mdata.ident == 'order_cost') {
        //orderslist_update_core.push(mdata.order_id, 'cost', mdata.cost);
    } else {
        //orderslist_update_core.refresh();
    }
}

function ws_unitsd_processor(mdata) {
}

function ws_webapibackend_processor(mdata) {
}

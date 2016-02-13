client_session = null;
function client_session_set(session) {
    if (session == client_session)
        return
    client_session = session;
    client_session_send(session);
}

function client_session_send(session, ws_) {
    if (!ws_)
        ws_ = wS;
    if (!ws_)
        return

    if (!session)
        session = client_session

    // TODO: Update client session in WS:
    console.log('Sending session: ' + session);
    wS.send(JSON.stringify({
        sessionid: session,
        command: "auth"
    }));
}

function show_loading_img(jQelem) {
    if (!jQelem)
        jQelem = $("#maincontent_wrapper");
    jQelem.html('<div class="width_middle_50"><img src="static/img/loading.gif" class="loading_img"></div>');
}


function admin_login() {

    var 
        uname_fld = $('.login_form_wrapper .username'),
        passwd_fld = $('.login_form_wrapper .passwd');
 
    if (!uname_fld.val()) {
        uname_fld.focus();
        return false;
    } else if (!passwd_fld.val()) {
        passwd_fld.focus();
        return false;
    }

    $.ajax(COMMON_URLS['login_test'], {
        type: 'POST',
        data: {
            'username': uname_fld.val(),
            'passwd': passwd_fld.val(),
        },
        
        statusCode: {
            403: function() {
                passwd_fld.val('');
                uname_fld.parent().addClass('login_error');
                passwd_fld.parent().addClass('login_error');
            },
            404: function() {
                alert( "page not found" );
            }
        },

        success: function(msg) {
            sammy_app.setLocation('#adminko/status');
        }
    })
     

}



function admin_geturl(url, params) {
    if (!params)
        params = {}
    if (!params.statusCode)
        params.statusCode = {}
                
    params.statusCode[401] = function() {
        console.log('unauthorized!');
        sammy_app.setLocation('#login');
    }
             
    var callback_ = null;
    if (params.success)
        callback_ = params.success;

    params.success = function(tpl) {
        if (callback_)
            callback_(tpl);
    }

    $.ajax(url, params);
}



function admin_load(jQwrapper, url, params) {
    if (!params)
        params = {}
    var callback_ = null;
    if (params.success)
        callback_ = params.success;

    params.success = function(tpl) {
        jQwrapper.hide();
        jQwrapper.html(tpl);
        jQwrapper.fadeIn();
        if (callback_)
            callback_(tpl);
    }
    admin_geturl(url, params);
}


function admin_load_part(part, route) {
    console.log('Calling part: ' + part);

    if (part == 'refresh') {
        console.log('Makeing refresh...');
        route.redirect('#adminko');
        sammy_app.refresh();

    } else if (part == 'status') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['admin_status']);
    } else if (part == 'nw_access_lists') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'nw_dhcp') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'nw_dns') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'sys_users') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['admin_sysusers']);
    } else if (part == 'sys_srv_vpn') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'sys_srv_dns') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'sys_srv_dhcp') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'notes') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'tools_speed') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'tools_ping') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    } else if (part == 'tools_traceroute') {
        admin_load($('.admin_content_wrapper'), COMMON_URLS['underconstruction']);
    }
}



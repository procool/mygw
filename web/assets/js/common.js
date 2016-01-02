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
            sammy_app.refresh();
        }
    })
     

}

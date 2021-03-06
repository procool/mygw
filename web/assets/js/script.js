var last_location = '';
var location_only_part = false;
var setTab = function(elem) {
    $(".tabs li").attr("id","");
    elem.parent().attr("id","current");
}

var sammy_app = $.sammy(function() {

    function load_cabinet () {
        setTab($(".tabs a.cabinet"));
        show_loading_img();
        $('#maincontent_wrapper').load(COMMON_URLS['cabinet'], null, function(tpl) {
            $(this).hide();
            $(this).html(tpl);
            $(this).fadeIn();
        });
    }

    function load_adminko (part, route) {
        setTab($(".tabs a.adminko"));
        var params = {};
        if (part)
            params.success = function(tpl) {
                admin_load_part(part, route);
            }
        admin_load($('#maincontent_wrapper'), COMMON_URLS['admin'], params);
    }


    this.bind('run-route', function(e, data) {
        var new_location = sammy_app.getLocation();
        if (last_location.match(/^\/#adminko/) && new_location.match(/^\/#adminko/)) 
            location_only_part = true;
        else
            location_only_part = false;
        last_location = new_location;
    });


    this.get('#adminko/:part', function(context, next) {
        if (!location_only_part)
            load_adminko(this.params['part'], this);
        else
            admin_load_part(this.params['part'], this);
    });

    this.get('#adminko', function(context, next) {
        this.redirect('#adminko/status');
    });

    this.get('/', function(context, next) {
        load_cabinet();
    });

    this.get('#cabinet', function(context, next) {
        load_cabinet();
    });


    this.get('#/cabinet/set/access/:acctype', function(context, next) {
        var acctype = this.params['acctype'];
        var this_ = this;
        $.getJSON(COMMON_URLS['cabinet_set_access_'+acctype], {}, function(data) {
            this_.redirect('#cabinet');
        });
    });


    this.get('#login', function(context, next) {
        $('#maincontent_wrapper').load(COMMON_URLS['login'])
    });

    this.get('#logout', function(context, next) {
        var this_ = this;
        $.ajax(COMMON_URLS['logout'], {
            statusCode: {
                403: function() {
                    this_.redirect('#adminko');
                }
            },
            success: function(msg) {
                client_session_set(null);
                this_.redirect('#adminko');
            }
        });
    });


});



$( document ).ready(function() {

    $('.tabs a').click(function(e) {
        setTab($(this));
    });



    if ("WebSocket" in window) {
        start_chat_ws(document.domain, '80', {onsuccess: function(ws_) {client_session_send(null, ws_)}});
    }

    

        
});


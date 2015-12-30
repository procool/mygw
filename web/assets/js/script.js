var sammy_app = $.sammy(function() {

    function load_cabinet () {
        show_loading_img();
        $('#maincontent_wrapper').load(COMMON_URLS['cabinet']);
    }



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


});



$( document ).ready(function() {

/*
    $(".js-open-order").on("click",function(){
        $(".js-main-section").show();
        $("body").css("overflow","hidden");
        $(".js-main-section").hide();
        $("body").css("overflow","auto");
        $(".js-confirm-popup").addClass("show");
        $(".js-confirm-popup").removeClass("show");
        $(".js-login-menu").toggle();
        $(this).next().toggle();
        $(".js-login-popup").show();
        $(".js-login-popup").hide();
        $( ".js-login-popup .input-field" ).each(function() {
          $(this).addClass("input-error");
        });
    });
*/
        
});


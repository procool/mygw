function show_loading_img(jQelem) {
    if (!jQelem)
        jQelem = $("#maincontent_wrapper");
    jQelem.html('<div class="width_middle_50"><img src="static/img/loading.gif" class="loading_img"></div>');
}


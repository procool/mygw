import logging

from misc.mixins import myTemplateView

class mainPageView(myTemplateView):
    template='mainpage/mainpage-ajax.tpl'


class jsUrlsView(myTemplateView):
    template='mainpage/urls_js-ajax.tpl'


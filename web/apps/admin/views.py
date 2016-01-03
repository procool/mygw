import logging
import datetime

from sqlalchemy import func, and_, or_, not_

from flask import url_for, session
from misc.mixins import myTemplateView, JSONView

from utils.arp_list import get_mac_by_ip

from models.all_models import InetEther
from models.session import session

from utils.server.http_client import HTTPClient
from libs.pfctl import PFCtl

from auth import LoginRequiredMixin, LoginRequiredRedirectMixin

class adminView(LoginRequiredMixin, myTemplateView):
    template='admin/admin-ajax.tpl'


class statusView(LoginRequiredMixin, myTemplateView):
    template='admin/status-ajax.tpl'


class shutdownView(LoginRequiredMixin, JSONView):
    __ctlsrv = HTTPClient(port=6999)
    
    def get_context_data(self, **kwargs):
        context = super(shutdownView, self).get_context_data(**kwargs)
        cmd = self.__cmd == 'poweroff' and 'poweroff' or 'reboot'
        r = self.__ctlsrv.call_handler('system/%s' % cmd)
        context['result'] = r
        return context
            
            
    def dispatch(self, request, command, *args, **kwargs):
        self.__cmd = command.lower()
        return super(shutdownView, self).dispatch(self, request, *args, **kwargs)


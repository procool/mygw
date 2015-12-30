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


class checkIPMixin(object):
    def check_for_ip(self):
        self.request.remote_ether = get_mac_by_ip(self.request.remote_addr)
        if self.request.remote_ether is None or self.request.remote_addr is None:
            return None

        addr = session.query(InetEther).filter(InetEther.mac==self.request.remote_ether).first()
        if addr is None:
            addr = InetEther()
            addr.mac = self.request.remote_ether
        if addr.ip != self.request.remote_addr or not addr.is_active:
            addr.ip = self.request.remote_addr
            addr.is_active = True
            addr.lastupdate = func.now()
            session.add(addr)
        addrs = session.query(InetEther).filter(not_(InetEther.mac==self.request.remote_ether))
        addrs = addrs.filter(InetEther.ip==self.request.remote_addr)
        addrs.update({"is_active": False})
        return addr


class cabinetView(checkIPMixin, myTemplateView):
    template='cabinet/cabinet-ajax.tpl'

    def get_context_data(self, **kwargs):
        addr = self.check_for_ip()
        context = super(cabinetView, self).get_context_data(**kwargs)
        context['addr_obj'] = addr
        if addr.access_type == 'tor':
            context['access_type'] = 'TOR'
        else:
            context['access_type'] = 'DIRECT'
        return context


class setIPView(checkIPMixin, JSONView):
    __ctlsrv = HTTPClient(port=6999)

    def get_context_data(self, **kwargs):
        context = super(setIPView, self).get_context_data(**kwargs)
        addr = self.check_for_ip()
        if addr is None:
            return context
        addr.access_type = self.__type
        session.add(addr)
        session.commit()
        r = self.__ctlsrv.call_handler('ip/%s/access' % self.request.remote_addr)
        context['result'] = r
        return context


    def dispatch(self, request, access_type, *args, **kwargs):
        if access_type in PFCtl.ip_proxy_types:
            self.__type = access_type
        else:
            self.__type = None
        return super(setIPView, self).dispatch(self, request, *args, **kwargs)

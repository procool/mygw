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

from auth import LoginRequiredMixin

class adminView(LoginRequiredMixin, myTemplateView):
    template='admin/admin-ajax.tpl'


import logging

from models.all_models import Users
from models.session import session

from misc.mixins import myTemplateView, JSONView
from misc.mixins_local.crud import ListViewBaseMixin
from auth import LoginRequiredMixin, LoginRequiredRedirectMixin



class usersView(LoginRequiredMixin, ListViewBaseMixin, myTemplateView):
    template='admin/users-ajax.tpl'
    model=Users
    list_name="users"



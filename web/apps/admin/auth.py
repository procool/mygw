import logging
import sha

from flask import redirect, url_for, abort, session as flask_session
from flaskcbv.view import View
from flaskcbv.response import Response
from flaskcbv.view.mixins import JSONMixin, getArgumentMixin



from misc.mixins import myTemplateView, JSONView

from models.all_models import Users
from models.session import session
from sessions import Sessions


class AuthMixin(object):
    def _check_for_auth(self):
        session_ = flask_session['session']
        uid = Sessions.check(session_)
        if uid is None:
            raise Exception('no such session!')
        user = session.query(Users).filter(Users.id==uid).first()
        if user is None:
            raise Exception('no such user!')
        self.request.user = user



class LoginRequiredRedirectMixin(AuthMixin):
    def prepare(self, *args, **kwargs):
        try:
            self._check_for_auth()
        except Exception as err:
            return redirect(url_for('admin:login'))
        return super(LoginRequiredRedirectMixin, self).prepare(*args, **kwargs)
      

class LoginRequiredMixin(AuthMixin):
    def prepare(self, *args, **kwargs):
        try:
            self._check_for_auth()
        except Exception as err:
            abort(403)
        return super(LoginRequiredMixin, self).prepare(*args, **kwargs)




class loginView(myTemplateView):
    template='admin/login-ajax.tpl'


class testloginView(getArgumentMixin, JSONMixin, View):
    AVALIBLE_METHODS = ["POST",]

    def get_context_data(self, **kwargs):
        return {
            'errno': 0,
            'error': 'Ok',
            'details': '',
        }

    def post(self, *args, **kwargs):
        try: 
            login = self.get_argument_smart('username', as_get=False, as_post=True, as_session=False, as_cookie=False)
            passwd = self.get_argument_smart('passwd', as_get=False, as_post=True, as_session=False, as_cookie=False)
        except Exception as err: 
            abort(403)

        try: 
            passwd = sha.new(passwd).hexdigest()
        except:
            abort(403)
        user = session.query(Users).filter(Users.login==login).filter(Users.passwd==passwd).first()
        if user is None:
            abort(403)

        flask_session['session'] = Sessions().create(user.id)

        return Response(self.get_as_json())




class logOutView(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        Sessions().delete(self.request.user.id)
        return Response(redirect(url_for('admin:login')))


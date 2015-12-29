import cron.py_path
from global_settings import settings
from models.session import session
#from models.all_models import Users, InetEther
from models.base import get_model

Users = get_model('users.Users')

#u = Users(login='admin')
#session.add(u)
#session.commit()
#session.query(Users).filter(Users.login=='admin').delete()

print settings
print session




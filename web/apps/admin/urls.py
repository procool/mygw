from flaskcbv.url import Url, make_urls
from views import adminView
from auth import loginView, testloginView, logOutView

from views import statusView, shutdownView


namespases = make_urls(
    Url('', adminView(), name="main"),
    Url('login/', loginView(), name="login"),
    Url('login/test/', testloginView(), name="login_test"),
    Url('logout/', logOutView(), name="logout"),
    Url('status/', statusView(), name="status"),
    Url('system/shutdown/<command>/', shutdownView(), name="system_shutdown"),
)




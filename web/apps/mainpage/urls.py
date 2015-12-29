from flaskcbv.url import Url, make_urls
from views import mainPageView
from views import setIPView

namespases = make_urls(
    Url('', mainPageView(), name="main"),
    Url('set/access/<access_type>/', setIPView(), name="set_ip"),
)




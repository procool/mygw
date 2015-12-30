from flaskcbv.url import Url, make_urls
from views import cabinetView
from views import setIPView

namespases = make_urls(
    Url('', cabinetView(), name="main"),
    Url('set/access/<access_type>/', setIPView(), name="set_access"),
)




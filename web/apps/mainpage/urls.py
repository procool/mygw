from flaskcbv.url import Url, make_urls
from views import mainPageView, jsUrlsView

namespases = make_urls(
    Url('', mainPageView(), name="main"),
    Url('urls', jsUrlsView(), name="urls"),
)




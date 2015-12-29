from flaskcbv.url import Url, include, make_urls

import mainpage.urls

namespases = make_urls(
    Url('/', include(mainpage.urls.namespases, namespace='mainpage')),
)


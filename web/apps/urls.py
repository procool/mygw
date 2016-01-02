from flaskcbv.url import Url, include, make_urls

import mainpage.urls
import cabinet.urls
import admin.urls

namespases = make_urls(
    Url('/', include(mainpage.urls.namespases, namespace='mainpage')),
    Url('/cabinet/', include(cabinet.urls.namespases, namespace='cabinet')),
    Url('/admin/', include(admin.urls.namespases, namespace='admin')),
)


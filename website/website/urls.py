from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^bbsadmin/', include(admin.site.urls)),
    url(r'^bbs/', include('Main.urls')),
]

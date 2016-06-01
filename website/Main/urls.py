from django.conf.urls import *

urlpatterns = patterns('Main.views',
        url(r'home','Home'),
        url(r'article_add/$','ArticleNew'),
        url(r'article_(\d+)/$','ArticleDetail'),
        url(r'^(\w+)/$','ArticleList'),
        url(r'^user/',include('User.urls')),
        url(r'^$','Home'),
)

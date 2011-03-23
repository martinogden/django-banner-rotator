from django.conf.urls.defaults import *

urlpatterns = patterns('banner_rotator.views',
    url(r'^click/(?P<banner_id>\d{1,4})/$', 'click', name='banner_click'),
)

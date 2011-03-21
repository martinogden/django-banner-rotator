from django.conf.urls.defaults import *

urlpatterns = patterns('adto.views',
    url(r'^click/(?P<banner_id>\d{1,4})/$', 'click', name='banner_click'),
)

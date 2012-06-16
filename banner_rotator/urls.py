#-*- coding:utf-8 -*-

try:
    # Django 1.4
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('banner_rotator.views',
    url(r'^click/(?P<banner_id>\d{1,4})/$', 'click', name='banner_click'),
)

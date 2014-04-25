# -*- coding: utf-8 -*-
__author__ = 'icecream'

from django.conf.urls import patterns, include, url

import views as data

urlpatterns = patterns(
    '',
    ('^$', data.hello,),
    ('^room/(?P<room_id>\d+)/$', data.room,),
    ('^room/(?P<room_id>\d+)/latest_data/$', data.latest_data,),
    ('^sensor/(?P<sensor_id>\d+)/$', data.sensor,),
    ('^download/$', data.download,),
)

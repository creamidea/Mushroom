# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views as controller

urlpatterns = patterns('',
    url(r'^$', controller.hello, ),
    # 控制/获取设备状态
    url(r'^(?P<controller_id>\d+)/$', controller.controller),
    # 获得房间设备列表
    url(r'^list/room/(?P<room_id>\d+)/$', controller.room_controller_list),
    # 获取列表
    url(r'^list/$', controller.controller_list),
    url(r'^update/room/(?P<room_id>\d+)/$', controller.room_controller_update),
    url(r'^sync/room/(?P<room_id>\d+)/$', controller.sync),
)

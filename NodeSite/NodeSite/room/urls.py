# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views as room

urlpatterns = patterns(
    '',
    url(r'^$', room.view,),
    # 获取房间列表
    url(r'^list/$', room.roomlist, ),
    # 获取房间信息
    url(r'^(?P<room_id>\d+)/$', room.room,),
    # 修改房间名称
    url(r'^(?P<room_id>\d+)/name/$', room.name),
    # 获取房间描述列表
    url(r'^description/list/$', room.desc_list),
)

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views as policy

urlpatterns = patterns(
    '',
    url(r'^$', policy.create, ),
    # 所有策略列表
    url(r'^list/$', policy.list, ),
    # 查看指定房间这在执行的策略，仅对房间单位有效
    url(r'now/room/(?P<room_id>\d+)/$', policy.now, ),
    # 对于策略本身的操作：增加，删除和修改
    url(r'(?P<policy_id>\d+)/$', policy.policy, ),
    # 策略的描述
    url(r'(?P<policy_id>\d+)/description/$', policy.description),
)
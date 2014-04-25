# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import views as policy

urlpatterns = patterns(
    '',
    url(r'^$', policy.create, ),
    url(r'^create/$', policy.create, ),
    # 所有策略列表
    url(r'^list/$', policy.policy_list, ),
    url(r'^room/(?P<room_id>\d+)/$', policy.policy_room_list, ),
    # 查看指定房间这在执行的策略，仅对房间单位有效
    url(r'^now/room/(?P<room_id>\d+)/$', policy.now, ),
    # 对于策略本身的操作：增加，删除和修改
    url(r'^(?P<policy_id>\d+)/$', policy.policy, ),
    url(r'^(?P<policy_id>\d+)/now/$', policy.ajax_now_by_policy_id, ),
    url(r'^(?P<policy_id>\d+)/plan/list/$', policy.get_plan_list, ),
    url(r'^(?P<policy_id>\d+)/done/list/$', policy.get_done_list, ),
    # 策略的描述
    url(r'^(?P<policy_id>\d+)/description/$', policy.description),
    # url(r'/room/(?P<policy_id>\d+)/', policy.room),
    url(r'^save/output/$', policy.save_output),
    url(r'^delete/output/$', policy.delete_output),

    # 策略实例处理
    url(r'^instance/create/$', policy.create_policy_instance),
    url(r'^instance/(?P<piid>\d+)/$', policy.policy_instance),
    url(r'^instance/(?P<piid>\d+)/output/save/$', policy.policy_instance_output_save),
    url(r'^instance/(?P<piid>\d+)/image/save/$', policy.policy_instance_image_save),
)

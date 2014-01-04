# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from NodeSite import settings 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # 账户设置，系统设置
    url(r'^accounts/', include('NodeSite.accounts.urls')),
    url(r'^mushroom/', include('NodeSite.mushroom.urls')),
)

urlpatterns += patterns('NodeSite.views',
    # 首页
    url(r'^$', 'home', name='home'),
    # 用户登录/登出  
    url(r'^login/$', 'login', name='login'),
    url(r'^login-test/$', 'login_test', name="login_test"),
    url(r'^logout/$', 'logout', name='logout'),

    # 房间信息
    url(r'^room/list/$', 'get_rooms', name="get_rooms"),
    url(r'^room/(\d+)/controller/list/$', 'get_room_controller_list',),
    url(r'^room/(\d+)/controller/(\d+)/$', 'get_room_controller',),

    # 搜索
    url(r'^search/$', 'search', name="search"),

    # 养殖策略
    url(r'^policy/now/room/(\d+)/$', 'get_now_policy_by_room_id',),
    url(r'^policy/list/$', 'policy_list',),
    url(r'^policy/(\d+)/$', 'policy_view',),
    url(r'^policy/$', 'policy_view'),

    # 控制器
    url(r'^controller/list/room/(\d+)/$', 'controller_list_view'),
    url(r'^controller/(\d+)/$', 'controller_view'),

    # 配置文件设置
    url(r'^config/log/(\w+)$', 'config_log'),
    
)

if settings.DEBUG:
    # Test
    # url(r'^NodeSite/', include('NodeSite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # test message
    urlpatterns += patterns('NodeSite.views',
                            (r'^playlist/create/$', 'create_playlist'),
    )

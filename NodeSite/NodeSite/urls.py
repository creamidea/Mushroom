# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from NodeSite import settings 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from NodeSite.views import home
urlpatterns = patterns('',
    # 账户设置，系统设置
    url(r'^$', home, name="home"),
    url(r'^account/', include('NodeSite.account.urls')),
    url(r'^room/', include('NodeSite.room.urls')),
    url(r'^plant/', include('NodeSite.plant.urls')),
    url(r'^sensor/', include('NodeSite.sensor.urls')),
    url(r'^controller/', include('NodeSite.controller.urls')),
    url(r'^policy/', include('NodeSite.policy.urls')),
    url(r'^search/', include('NodeSite.search.urls')),
    url(r'^data/', include('NodeSite.data.urls')),
    url(r'^system/', include('NodeSite.system.urls')),
)

urlpatterns += patterns('NodeSite.views',
    # 首页
    url(r'^signal-page/$', 'signal_page'),
    # 用户登录/登出  
    url(r'^login/$', 'login', name='login'),
    url(r'^login-test/$', 'login_test', name="login_test"),
    url(r'^logout/$', 'logout', name='logout'),

    # 用户注册
    url(r'^register/$', 'register', name='register'),

    # 修改名称
    url(r'^([\w]+)/(\d+)/name/$', 'update_name',),

    # 房间信息
    url(r'^room/list/$', 'get_rooms', name="get_rooms"),
    # url(r'^room/(\d+)/controller/list/$', 'get_room_controller_list',),
    # url(r'^room/(\d+)/controller/(\d+)/$', 'get_room_controller',),

    # 获取数据
    url(r'^data/room/(\d+)/$', 'get_data'),
    
    # 搜索
    url(r'^search/$', 'search', name="search"),

    # 养殖策略
    url(r'^policy/now/room/(\d+)/$', 'get_now_policy_by_room_id',),
    url(r'^policy/now/room/(\d+)/timepoint/$', 'get_now_time_point',),
    url(r'^policy/list/$', 'policy_list',),
    url(r'^policy/(\d+)/$', 'policy_view',),
    url(r'^policy/$', 'policy_view'),

    # 控制器
    url(r'^controller/list/room/(\d+)/$', 'controller_list_view'),
    url(r'^controller/(\d+)/$', 'controller_view'),

    # 配置文件设置
    url(r'^config/log/(\w+)$', 'config_log'),
    
)

# from article.views import ArticleDetailView

if settings.DEBUG:
    urlpatterns += patterns('',
    # Test
    # url(r'^NodeSite/', include('NodeSite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^mushroom/', include('NodeSite.mushroom.urls')),
    url(r'^webchat/', include('NodeSite.webchat.urls')),
    )
    # test message
    urlpatterns += patterns('NodeSite.views',
                            (r'^playlist/create/$', 'create_playlist'),
    )

    # urlpatterns += patterns('',
    #     url(r'^(?P<slug>[-_\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    # )


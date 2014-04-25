# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
# from django.contrib.auth.views import (password_change, password_change_done)

from .views import (signin, signout, signup, profile, manage, password_change, password_change_done, account_delete, profile_change)

# 账户设置，系统设置 
urlpatterns = patterns('',
    url(r'^login/$', signin, name='signin'),                #登录
    url(r'^logout/$', signout, name='signout'),                #退出
    url(r'^signup/$', signup, name='signup'),                #注册
    url(r'^profile/$', profile, name='profile'),                #用户信息
    url(r'^manage/$', manage, name='manage'),                #用户信息
    url(r'^password/change/$', password_change, name='password_change'),   #更改密码
    url(r'^password/change/done/$', password_change_done),   #更改密码
    # url(r'^change/password/$', password_change(request, 'profile.html')),   #更改密码
    # url(r'^change/password/done/$', password_change_done(request, 'profile.html'),)   #更改密码
    url(r'^profile/change/$', profile_change, name='profile_change'),
    url(r'^delete/$', account_delete, name="delete"),
)

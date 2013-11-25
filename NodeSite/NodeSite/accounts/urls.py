# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
# 账户设置，系统设置 
urlpatterns += patterns('',
    url(r'^login/$', 'signin', name='signin'),                #登录
    url(r'^logout/$', 'signout', name='signout'),                #退出
    url(r'^signup/$', 'signup', name='signup'),                #注册
    url(r'^profile/$', 'profile', name='profile'),                #用户信息

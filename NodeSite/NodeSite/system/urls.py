# -*- coding: utf-8 -*-
__author__ = 'icecream'

from django.conf.urls import patterns, include, url

import views as system

urlpatterns = patterns(
    '',
    ('^$', system.hello,),
    ('^log/(?P<type>(\w+))/$', system.log, ),
)
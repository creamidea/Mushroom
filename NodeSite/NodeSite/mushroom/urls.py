# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import settings

urlpatterns = patterns('',
    url(r'^settings/$', settings, name='m_settings'),
)
                        

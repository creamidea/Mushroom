# -*- coding: utf-8 -*-
__author__ = 'icecream'

from django.conf.urls import patterns, include, url

import views as search

urlpatterns = patterns(
    '',
    ('^$', search.view, ),
    ('^room/(?P<room_id>\d+)$', search.room, ),
)
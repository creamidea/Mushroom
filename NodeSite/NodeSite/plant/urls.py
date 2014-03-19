# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views as plant

urlpatterns = patterns(
    '',
    url(r'^$', plant.hello, ),
    url(r'^list/$', plant.list, ),
    url(r'^(?P<plant_id>\d+)/$', plant.plant,),
)

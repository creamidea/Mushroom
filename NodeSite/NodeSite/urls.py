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
    url(r'^$', 'home', name='home'),
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

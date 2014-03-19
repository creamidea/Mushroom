# from django.conf.urls.defaults import *
from django.conf.urls import *
from . import settings
from .chat import views

urlpatterns = patterns('',
                       ('^$', views.main),
                       ('^a/message/new$', views.message_new),
                       ('^a/message/updates$', views.message_updates))

urlpatterns += patterns('django.views.static',
                        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), 'serve',
                         {'document_root': settings.MEDIA_ROOT,
                          'show_indexes': True}))

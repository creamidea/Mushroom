#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from django.core.management import execute_from_command_line, call_command
# 将其安全转成协程gevent
# from gevent import monkey
# monkey.patch_all()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NodeSite.settings")
    execute_from_command_line(sys.argv)

# #####################################################################
# 测试gevent
# import os
# import sys
# from gevent import monkey; monkey.patch_all()
# from gevent.wsgi import WSGIServer
#
# # from django.core.management import execute_from_command_line
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NodeSite.settings")
# # execute_from_command_line(sys.argv)
#
# from django.core.management import setup_environ
# import settings
# setup_environ(settings)
#
# from django.core.handlers.wsgi import WSGIHandler as DjangoWSGIApp
# application = DjangoWSGIApp()
# server = WSGIServer(("127.0.0.1", 1234), application)
# print "Starting server on http://127.0.0.1:1234"
# server.serve_forever()

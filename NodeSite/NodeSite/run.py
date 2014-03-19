#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey;
monkey.patch_all()
from gevent import wsgi
from wsgi import wsgi as application
HOST = '127.0.0.1'
PORT = 8000
# set spawn=None for memcache
wsgi.WSGIServer((HOST, PORT), application).serve_forever()

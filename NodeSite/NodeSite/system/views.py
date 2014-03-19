# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

import gevent
from gevent.event import Event

evt = Event()

def setter():
    '''After 3 seconds, wake all threads waiting on the value of evt'''
    print('A: Hey wait for me, I have to do something')
    gevent.sleep(5)
    print("Ok, I'm done")
    evt.set()

def waiter():
    '''After 3 seconds the get call will unblock'''
    print("I'll wait for you")
    evt.wait()  # blocking
    print("It's about time")
    return HttpResponse("Here is system control center")

def main():
    print "Here is main()"
    # gevent.joinall([
    #     gevent.spawn(setter),
    #     gevent.spawn(waiter),
    #     gevent.spawn(waiter),
    #     gevent.spawn(waiter),
    #     gevent.spawn(waiter),
    #     gevent.spawn(waiter),
    # ])

def hello(request):
    # gevent.joinall([
    #     gevent.spawn(setter),
    # ])
    # setter()
    evt.wait(0)  # blocking
    print("It's about time")
    title = u"系统控制界面"
    return render(request,
                      "system.html",
                      dict(
                          title=title,
                      ),
    )

def log(request, type="error"):
    return HttpResponse("You request the type of log is %s" % type)

def warning(request):
    return HttpResponse("Hello, world")
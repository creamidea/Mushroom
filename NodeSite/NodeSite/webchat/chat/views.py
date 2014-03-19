# -*- coding: utf-8 -*-

import uuid
import simplejson
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.context_processors import csrf
import gevent
from gevent.event import Event
# from gevent import monkey
# monkey.patch_all()
# import gevent.monkey
# gevent.monkey.patch_all(httplib=False)
from .. import settings

evt = Event()
cache = []
cache_size = 200

class ChatRoom(object):
    cache_size = 200

    def __init__(self):
        self.cache = []
        self.new_message_event = Event()

    def main(self, request):
        # 这里是处理静态文件，估计是django1.4-的处理方式
        if self.cache:
            request.session['cursor'] = self.cache[-1]['id']
        return render_to_response('webchat.html', {'MEDIA_URL': settings.MEDIA_URL, 'messages': self.cache})

    def message_new(self, request):
        name = request.META.get('REMOTE_ADDR') or 'Anonymous'
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # print forwarded_for
        if forwarded_for and name == '127.0.0.1':
            name = forwarded_for
        msg = create_message(name, request.POST['body'])
        self.cache.append(msg)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]
        self.new_message_event.set()
        self.new_message_event.clear()
        return json_response(msg)

    def message_updates(self, request):
        cursor = request.session.get('cursor')
        print "//////////////////////////////"
        print "cursor:", cursor

        if not self.cache or cursor == self.cache[-1]['id']:
            self.new_message_event.wait() # 这里等唤醒。

        assert cursor != self.cache[-1]['id'], cursor
        try:
            print "//////////////////////////////"
            for index, m in enumerate(self.cache):
                if m['id'] == cursor:
                    # 自己的
                    data_ = json_response({'messages': self.cache[index + 1:]})
            data_ = json_response({'messages': self.cache})
            return data_
        except Exception, e:
            print e
        finally:
            if self.cache:
                request.session['cursor'] = self.cache[-1]['id']
            else:
                request.session.pop('cursor', None)

room = ChatRoom()
main = room.main
message_new = room.message_new
message_updates = room.message_updates

# def main(request):
#     return room.main(request)


# def message_new(request):
#     global cache
#     # global evt
#     name = request.META.get('REMOTE_ADDR') or 'Anonymous'
#     forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     # print forwarded_for
#     if forwarded_for and name == '127.0.0.1':
#         name = forwarded_for
#     msg = create_message(name, request.POST['body'])
#     cache.append(msg)
#     if len(cache) > cache_size:
#         cache = cache[-cache_size:]
#         # self.new_message_event.set()
#         # self.new_message_event.clear()
#     evt.set()
#     evt.clear()
#     return json_response(msg)
#     # gevent.joinall([gevent.spawn(room.message_new, request)])
#     # return room.message_new(request)
# def message_updates(request):
#     evt.wait(5)
#     # gevent.sleep(2)
#     return HttpResponse("hello, world")
#     # global cache
#     #
#     # cursor = request.session.get('cursor')
#     # print "//////////////////////////////"
#     # print "cursor:", cursor
#     #
#     # # self.new_message_event.wait() # 这里等唤醒。
#     #
#     # if not cache or cursor == cache[-1]['id']:
#     #     evt.wait()
#     #     # print "cache:", self.cache
#     #     # if self.new_message_event.is_set():
#     #     #     print "Before new message event"
#     #     # self.new_message_event.wait() # 这里等唤醒。
#     #
#     # # while True:
#     # #     pass
#     #
#     #
#     # # print enumerate(self.cache)
#     # # assert cursor != self.cache[-1]['id'], cursor
#     # try:
#     #     print "//////////////////////////////"
#     #     for index, m in enumerate(cache):
#     #         if m['id'] == cursor:
#     #             # 自己的
#     #             data_ = json_response({'messages': cache[index + 1:]})
#     #     data_ = json_response({'messages': cache})
#     #     return data_
#     # except Exception, e:
#     #     print e
#     # finally:
#     #     if cache:
#     #         request.session['cursor'] = cache[-1]['id']
#     #     else:
#     #         request.session.pop('cursor', None)
#
#     # gevent.joinall([gevent.spawn(room.message_updates, request)])
#     # return room.message_updates(request)

# gevent.joinall([
#     gevent.spawn(message_new),
#     gevent.spawn(message_updates),
# ])

def create_message(from_, body):
    data = {'id': str(uuid.uuid4()), 'from': from_, 'body': body}
    data['html'] = render_to_string('message.html', dictionary={'message': data})
    return data


def json_response(value, **kwargs):
    kwargs.setdefault('content_type', 'text/javascript; charset=UTF-8')
    return HttpResponse(simplejson.dumps(value), **kwargs)

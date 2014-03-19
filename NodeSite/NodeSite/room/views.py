# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
# from NodeSite.db.db_operator import db_inst as db
from NodeSite.db import db_operator as db
from .models import RoomManagy

from ..decorators import json_response


def hello(request):
    return HttpResponse("Hello, world")

def view(request):
    return render(request,
                  "room-list.html",
                  {
                      "title":"房间列表",
                   }
    )

@json_response
def roomlist(request):
    # rm = RoomManagy()
    data = db.get_all_room()
    # print "[ROOM LIST DATA:]", data
    return dict(code=0, body=data)

@json_response
def ajax_room(request, room_id):
    data = db.get_room_info(room_id)
    return dict(body=data)

def room(request, room_id):
    if request.is_ajax():
        return ajax_room(request, room_id)
    else:
        title = u"房间%s信息" % room_id
        return render(request,
                      "room-item.html",
                      dict(
                          title=title,
                          room_id=room_id,
                      ),
        )

@json_response
def name(request, room_id):
    "关于房间名字的相关操作"
    if request.method == 'GET':
        return dict(body="get room name")
    elif request.method == 'POST':
        return dict(body="create room name")
    elif request.method == 'PUT':
        new_description = "test"
        result = db.update_room_name(room_id, new_description)
        return dict(code=result)

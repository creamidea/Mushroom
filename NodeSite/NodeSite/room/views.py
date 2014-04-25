# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
# from NodeSite.db.db_operator import db_inst as db
from NodeSite.db.db_operator import DbOperator
from .models import RoomManagy

from ..decorators import json_response

# db = DbOperator()

def hello(request):
    return HttpResponse("Hello, world")

def view(request):
    return render(request,
                  "room-list.html",
                  {
                      "title":"房间列表",
                   }
    )


def roomlist(request):
    # rm = RoomManagy()
    if request.is_ajax():
        return ajax_roomlist(request)
    else:
        return HttpResponse("hello")
    # print "[ROOM LIST DATA:]", data

@json_response
def ajax_roomlist(request):
    db = DbOperator()
    data = db.get_all_room()
    return dict(code=0, body=data)

@json_response
def ajax_room(request, room_id):
    db = DbOperator()
    data = db.get_room_info(room_id)
    # print "[ajax_room]", data
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
        db = DbOperator()
        result = db.update_room_name(room_id, new_description)
        return dict(code=result)

@json_response
@login_required
@require_GET
def desc_list(request):
    db = DbOperator()
    room_desc_list = db.room_dict
    return dict(body=room_desc_list)

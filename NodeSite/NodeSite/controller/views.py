# -*- coding: utf-8 -*-

# Create your views here.
from threading import Timer
import time
import re
import json

from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from NodeSite.settings import MIDDLEWARE_ADDRESS as ADDRESS
from ..decorators import json_response
from ..db.db_operator import DbOperator
from communicate import Communicate, SyncService

db = DbOperator()

# 系统启动时运行

# comm.update()
# 启动同步信道
# syncService = SyncService(ADDRESS)
# syncService.start()

def hello(request):
    return HttpResponse("Hello, world")

@json_response
@login_required
def controller(request, controller_id):
    # 对单个控制器的操作
    code = -1
    if request.method == 'GET':
        data = "You will get the state of controller %s " % controller_id
    elif request.method == 'PUT':
        # 开关一个设备
        put = QueryDict(request.body)
        action = put.get('action')
        print controller_id, action
        # 这个信道用于发送
        comm = Communicate(ADDRESS)
        comm.connect()
        data = comm.send_and_receive(controller_id, action)
        comm.close()
        # print data
        if isinstance(data, str):
            if re.match(r'.*error.*', data, re.I):
                code = -1
            if re.match(r'.*not.*', data, re.I):
                code = -1
        elif isinstance(data, tuple):
            # print "is tuple:", data
            code = json.loads(data[0]).get("code", -1)
        
        # pkg = control_package(controller_id, action)
        # print pkg
        # data = "You will change the state of controller of %s" % controller_id
    else:
        data = u"未知操作"
        code = -1
    return dict(code=code, body=data)


@login_required
def controller_list(request):
    if request.is_ajax():
        return ajax_controller_list(request)
    else:
        return render(request, 'controller-list.html',
                      {'title': u'控制器列表'})

@json_response
@login_required
def ajax_controller_list(request):
    # 所有控制器的列表
    if request.method == 'GET':
        data = [
    {
        "roomId": 1,
        "controllerId": 1,
        "controllerType": "风机",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 2,
        "controllerType": "加湿器",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 3,
        "controllerType": "温度控制器",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 4,
        "controllerType": "LED控制",
        "state": "on",
    },
    ]
    return dict(body = data)

@login_required
def room_controller_list(request, room_id):
    if request.is_ajax():
        return ajax_room_controller_list(request, room_id)
    else:
        title = u"房间%s控制面板" % room_id
        return render(request,
                      "controller-item.html",
                      dict(
                          title=title,
                          room_id=room_id,
                      ),
        )
@json_response
@login_required
def ajax_room_controller_list(request, room_id):
    # 房间里面控制器列表
    data = [
    {
        "roomId": room_id,
        "controllerId": 1,
        "controllerType": "风机",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 12,
        "controllerType": "风机2",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 2,
        "controllerType": "加湿器",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 3,
        "controllerType": "温度控制器",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 13,
        "controllerType": "温度控制器2",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 4,
        "controllerType": "LED控制",
        "state": "on",
    },
    ]
    data = db.get_room_controllers(room_id)
    return dict(body=data)

@json_response
@login_required
def room_controller_update(request, room_id):
    print ">>>>>>>here is controller update"
    
    # 这里是更新处理函数
    data = [
    {
        "roomId": room_id,
        "controllerId": 1,
        "controllerType": "风机",
        "state": "on",
    },
    {
        "roomId": room_id,
        "controllerId": 2,
        "controllerType": "加湿器",
        "state": "off",
    },
    {
        "roomId": room_id,
        "controllerId": 3,
        "controllerType": "温度控制器",
        "state": "off",
    },
    {
        "roomId": room_id,
        "controllerId": 4,
        "controllerType": "LED控制",
        "state": "on",
    },
    ]
    return dict(body=data)

@json_response
@login_required
def sync(request, room_id):
    # 这里是和中间件同步函数
    print "syncing..."
    # data = syncService.update(room_id)
    # return dict(body=data)



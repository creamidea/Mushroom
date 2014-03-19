# -*- coding: utf-8 -*-

# Create your views here.
# from threading import time

from django.http import HttpResponse, QueryDict
from NodeSite.settings import MIDDLEWARE_ADDRESS as ADDRESS
from ..decorators import json_response
from communicate import Communicate, SyncService
# from gevent.event import Event

# 这个用于存储所有控制器的状态
# 这里可能使得房间与设备绑定了，后期可能会遇到一些问题
# 但是在我现在看来，应该这里没有问题
# {[:roomId]: ([signature], [notice object/channel])}
rooms = {}

# 系统启动时运行
comm = Communicate(ADDRESS)
comm.connect()
# comm.update()

# 启动同步信道
# syncService = SyncService(ADDRESS)
# sync.start()

def hello(request):
    return HttpResponse("Hello, world")

@json_response
def controller(request, controller_id):
    # 对单个控制器的操作
    if request.method == 'GET':
        data = "You will get the state of controller %s " % controller_id
    elif request.method == 'PUT':
        # 开关一个设备
        put = QueryDict(request.body)
        action = put.get('action')
        print controller_id, action
        data = comm.send_and_receive(controller_id, action)
        print data
        # pkg = control_package(controller_id, action)
        # print pkg
        # data = "You will change the state of controller of %s" % controller_id
    else:
        data = "Unkown operation"
    return dict(body=data)

@json_response
def controller_list(request):
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

@json_response
def room_controller_list(request, room_id):
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
        "controllerId": 4,
        "controllerType": "LED控制",
        "state": "on",
    },
    ]
    return dict(body=data)

@json_response
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
def sync(request, room_id):
    # 这里是和中间件同步函数
    print "syncing..."
    data = syncService.update(room_id)
    return dict(body=data)

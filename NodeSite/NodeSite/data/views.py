# -*- coding: utf-8 -*-
# Create your views here.

from datetime import (datetime, timedelta)

from django.http import HttpResponse
from ..decorators import json_response
from ..db import db_operator as db

def hello(request):
    return HttpResponse("Here is search")

@json_response
def room(request, room_id):
    # 查询房间环境变化
    request_get = request.GET
    start_time = request_get.get("startTime")
    end_time = request_get.get("endTime")
    if start_time is None and end_time is None:
        end_time = datetime.now()
        one_hour = timedelta(hours=1)
        start_time = end_time - one_hour
    print start_time, " to ", end_time
    data = db.get_time_range_data(room_id, start_time, end_time)
    return dict(body=data)

@json_response
def sensor(request, sensor_id):
    # 按传感器编号查询
    request_get = request.GET
    start_time = request_get.get("startTime")
    end_time = request_get.get("endTime")
    if start_time is None and end_time is None:
        end_time = datetime.now()
        one_hour = timedelta(hours=1)
        start_time = end_time - one_hour
    print start_time, " to ", end_time
    data = "hello, world"
    return dict(body=data)
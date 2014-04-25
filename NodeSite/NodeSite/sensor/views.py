# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from ..decorators import json_response
# from NodeSite.db import db_operator as db
from ..db.db_operator import DbOperator

db = DbOperator()

def hello(request):
    return HttpResponse("Hello, world")

def sensor(request, sensor_id):
    title = u"传感器%s信息" % sensor_id
    return render(request,
                      "sensor-item.html",
                      dict(
                          title=title,
                          sensor_id=sensor_id,
                      ),
    )
@json_response
def average(request):
    data = db.get_average()
    return dict(body=data)

@json_response
def room_sensor_list(request, room_id):
    data = db.get_room_sensors(room_id)
    # return data
    return dict(body=data)
    
    

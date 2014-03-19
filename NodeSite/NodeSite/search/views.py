# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from ..decorators import json_response
from ..db import db_operator as db

@json_response
@require_GET
def view(request):
    request_get = request.GET
    room_id = request_get.get("roomId")
    plant_id = request_get.get("plantId")
    sensor_type = request_get.get("sensorType")
    start_time = request_get.get("startTime")
    end_time = request_get.get("endTime")
    # print room_id, plant_id, sensor_id
    if room_id and start_time and end_time:
        data = db.get_time_range_data(
            room_id, start_time, end_time)
        return dict(body=data)
    # elif room_id &&


@json_response
def room(request, room_id):
    data = "You search room %s" % room_id
    return dict(body=data)


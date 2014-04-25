# -*- coding: utf-8 -*-
# Create your views here.
import xlwt
import logging
from datetime import (datetime, timedelta)

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ..decorators import json_response
from ..db.db_operator import DbOperator

# logging.basicConfig(level=logging.DEBUG)
# def debug(param):
#     logging.debug('')
    

def hello(request):
    return HttpResponse("Here is search")

@json_response
@login_required
def room(request, room_id):
    # 查询房间环境变化
    request_get = request.GET
    start_time = request_get.get("startTime")
    end_time = request_get.get("endTime")
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print start_time, " to ", end_time
    db = DbOperator()
    data = db.get_time_range_data(int(room_id), start_time, end_time)
    # print "[data/views.py]:", data
    if len(data) < 1:
        if request.is_ajax():
            return dict(code=-1)
    return dict(body=data)

@json_response
@login_required
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
    db = DbOperator()
    data = db.certain_sensor_time_range_data(int(sensor_id), start_time, end_time)
    if data["sensorType"] == "":
        if request.is_ajax():
            return dict(code=-1)
            # raise Http404()
        else:
            HttpResponseRedirect('/404.html')
    else:
        print ">>>>", data
        return dict(body=[data])

@json_response
@login_required
def latest_data(request, room_id):
    db = DbOperator()
    data = db.get_latest_data(int(room_id))
    return dict(body=data)

@login_required
def download(request):
    get = request.GET
    room_id = get.get("roomId")
    sensor_id = get.get("sensorId")
    start_time = get.get("startTime")
    end_time = get.get("endTime")
    if start_time is None and end_time is None:
        # 如果没有给出起止时间，则默认为今天
        end_time = datetime.now()
        one_hour = timedelta(hours=1)
        start_time = end_time - one_hour
    excel_file = xlwt.Workbook(encoding='utf8')
    db = DbOperator()
    if room_id is None and sensor_id is not None:
        # 这里下载单个传感器的值
        sheet = excel_file.add_sheet(u'传感器%s'%sensor_id)
        data = db.certain_sensor_time_range_data(int(sensor_id), start_time, end_time)
        if len(data) < 1:
            raise Http404()
        sensorType = data["sensorType"]
        sensorId = data["sensorId"]
        values = data["values"]
        sheet.write(0, 0, u"传感器%s:%s" % (sensorType, sensorId))
        sheet.write(1, 0, u"采集时间")
        sheet.write(1, 1, u"采集值")
        row = 2
        for item in values:
            sheet.write(row, 0, item[0])
            sheet.write(row, 1, item[1])
            row = row + 1
        filename = "%s:%s-%s" % (sensor_id, start_time, end_time)
        
    elif room_id is not None:
        # 这里下载房间中所有传感器的值
        data = db.get_time_range_data(int(room_id), start_time, end_time)
        if len(data) < 1:
            raise Http404()
        sheet = {}
        row = {}
        for sensor in data:
            print sensor
            sensorId = sensor.get("sensorId")
            sensorType = sensor.get("sensorType")
            values = sensor.get("values")
            if not sheet.has_key(sensorType):
                # 这里是以一种传感器创建一个sheet
                sheet[sensorType] = excel_file.add_sheet(u'房间%s传感器%s'%(room_id, sensorType))
            if not row.has_key(sensorType):
                row[sensorType] = 0
            # 以同种传感器的编号为分段条件
            sheet[sensorType].write(row[sensorType], 0, u"传感器:%s"%sensorId)
            row[sensorType] = row[sensorType] + 1
            sheet[sensorType].write(row[sensorType], 0, u"采集时间")
            sheet[sensorType].write(row[sensorType], 1, u"采集值")
            row[sensorType] = row[sensorType] + 1
            # sheet[sensorType].write(row[sensorType], 0, u"传感器编号：%s"%sensorId)
            for v in values:
                # 这里写入某个编号传感器的采集值
                sheet[sensorType].write(row[sensorType], 0, v[0].strftime("%Y/%m/%d %H:%M:%S"))
                sheet[sensorType].write(row[sensorType], 1, v[1])
                row[sensorType] = row[sensorType] + 1
            # print sensor, values
            # print "++++++++"
        filename = "%s:%s-%s" % (room_id, start_time, end_time)

    # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    # print sensor_id, start_time, end_time, data
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % filename
    excel_file.save(response)
    return response

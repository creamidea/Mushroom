# -*- coding: utf-8 -*-

# Create your views here.

def all_policy_info():
    data = [
    {
        "policyId": 1,
        "description": "养殖蘑菇1",
    },
    {
        "policyId": 2,
        "description": "养殖蘑菇2",
    },
    {
        "policyId": 3,
        "description": "养殖蘑菇3",
    },
    ]
    return data

def current_policy(room_id):
    data = {
        "roomId": room_id,
        "policyId": 1,
        "description": "我也不知道养什么啊",
        "policy": [
        {
        "date" : "2013-12-30",
        "hour" : "20:21",
        "temperature": (100, 200),
        "humidity": (10,20),
        "co2":(1,2),
        "brightness": ["blue"],
        },
        {
            "date" : "2013-12-31",
            "hour" : "20:21",
        "temperature": (100, 200),
        "humidity": (10,20),
        "co2":(1,2),
        "brightness": ["blue"],
        },
        {
            "date" : "2014-01-07",
            "hour" : "15:00",
        "temperature": (100, 200),
        "humidity": (10,20),
        "co2":(1,2),
        "brightness": ["blue"],
        },
        ]
    }
    return data

def new_policy_instance(**kwargs):
    return 0

def get_policy(policy_id):
    policy= [
            {
            "date" : "2",
            "hour" : "2",
            "temperature": (100, 200),
            "humidity":  (10, 20),
            "co2":  (1, 2),
            "brightness": "blue",
            },
            {
                "date" : "1",
                "hour" : "1",
            "temperature": (100, 200),
            "humidity":  (10, 20),
            "co2":  (1, 2),
            "brightness": "white",
            },
            ]
    return policy

def update_policy_desc(policy_id, description):
    return 0

def get_all_room():
    # TODO: 这里更改了部分的信息，需要告知数据库层
    context = [{
      "roomId": 1,
      "roomName": "房间1",
      "plantId": 1,
      "plantName": "蘑菇",
      "time": "2013-12-25 16:41",
      "average": dict(temperature=180, co2=24, humidity=150),
      "sensors": {
        'temperature': (1,2,3,4,5),
        'co2': (12,13,14,15),
        'humidity': (23,24,25,26,27),
      },
      "brightness": "blue",
      "nowPolicy": 1,
    },
    {
      "roomId": 2,
      "roomName": "房间2",
      "plantId": 2,
      "plantName": "蘑菇",
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
      "sensors": {
        'temperature': (1,2,3,4,5),
        'co2': (12,13,14,15),
        'humidity': (23,24,25,26,27),
      },
      "brightness": "yellow",
      "nowPolicy": 1,
    },
    {
      "roomId": 3,
      "roomName": "房间3",
      "plantId": 3,
      "plantName": "蘑菇",
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
      "sensors": {
        'temperature': (1,2,3,4,5),
        'co2': (12,13,14,15),
        'humidity': (23,24,25,26,27),
      },
      "brightness": "yellow",
      "nowPolicy": 1,
    }
    ]
    return context
def get_room_sensor_list(room_id):
    sensors = {
        'temperature': (1,2,3,4,5),
        'co2': (12,13,14,15),
        'humidity': (23,24,25,26,27),
    }
    return sensros
    
def get_room_info(room_id):
    context = {
      "roomId": room_id,
      "roomName": "房间1",
      "plantId": 1,
      "plantName": "蘑菇",
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
      "sensors": {
        'temperature': (1,2,3,4,5),
        'co2': (12,13,14,15),
        'humidity': (23,24,25,26,27),
      },
      "brightness": "blue",
      "nowPolicy": 1,
    }
    return context

def get_average():
    context = [{
        "roomId":1,
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
    },{
        "roomId":2,
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
    }, {
        "roomId":3,
      "time": "2013-12-25 16:41",
      "average": dict(temperature=18, co2=24, humidity=150),
    }]
    return context

# TODO: 通知数据库方面
# 数据返回值有所变化 2014-03-12
def get_time_range_data(room_id, start_time, end_time):
    data = [
        {
            "sensorId": 1,
            "sensorType": "temperature",
            "position": "上1",
            "values":
            (
                ("2014/01/08 21:08", 100),
                ("2014/01/08 21:09", 200),
                ("2014/01/08 21:15", 300),
               ("2014/01/08 22:15", 300),

            )
        },
        {
            "sensorId": 2,
            "sensorType": "temperature",
            "position": "上2",
            "values":
            (
                ("2014/01/08 21:08", 410),
                ("2014/01/08 21:09", 320),
                ("2014/01/08 21:15", 134),

            )
        },
        {
            "sensorId": 5,
            "sensorType": "temperature",
            "position": "上2",
            "values":
            (
                ("2014/01/08 21:08", 100),
                ("2014/01/08 21:09", 200),
                ("2014/01/08 21:15", 134),
                ("2014/01/08 21:22", 140),
                ("2014/01/08 21:34", 112),
                ("2014/01/08 21:45", 234),
                ("2014/01/08 21:56", 243),
                ("2014/01/08 22:01", 324),

            )
        },
        {
            "sensorId": 3,
            "sensorType": "humidity",
            "position": "上2",
            "values":
            (
                ("2014/01/08 21:08", 400),
                ("2014/01/08 21:09", 500),
                ("2014/01/08 21:15", 100),
            )
        },
    ]
    return data

def update_room_name(room_id, room_description):
    return 0

# -*- coding: utf-8 -*-
#reverse函数可以像在模板中使用url那样，在代码中使用
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)

from django.contrib import messages
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
# from django.contrib.auth.views import (login, logout)
from django.contrib.auth.models import (Group, Permission, User)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from functools import wraps
# from decorator import decorator
import json

def serialize(target="json"):
    """使用装饰器序列化参数"""
    _serialize = {
        "json": json.dumps,
    }
    def wrapper1(func):
        @wraps(func)
        def wrapper2(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                response = HttpResponse(_serialize[target](result))
            except:
                error = '{"code": %d, "definition": %s}' % (-1, u"序列化错误")
                response = HttpResponse(error)
            return response
        return wrapper2
    return wrapper1


def home(request):
    if not request.user.is_authenticated():
        return render(request,"login-1.html", dict(title="蘑菇房监控平台"))
    else:
        print ">>>>", request.path
        # return HttpResponseRedirect(redirect_to="/")
        return render(request,"index.html", dict(title="蘑菇房监控平台"))

# @login_required
def signal_page(request):
    """
    主页视图处理函数
    
    :param request: request对象
    :rtype: HttpResponse
    """
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    return render(request, 'mushroom.html')

def userpackage(user):
    mesg = {
        "gavatar": "static/img/photo.png",
        "userId": user.pk,
        "username": user.username,
        "groupId": "1",
        "groupName":"Admin",
        "menu": [
            {"url": "#mushroom", "name": u"蘑菇房"},
            {"url": "#profile", "name": u"个人信息"},
            {"url": "#log", "name": u"日志"},
            {"url": "#setting", "name": u"系统设置"},
            {"url": "#logout", "name": u"退出"},
        ],
        "copyright": "CSLG",
        "version": "v0.0.1",
    }
    return mesg

@serialize("json")
@require_POST
def login_test(request):
    """
    测试用户是否登录
    
    :param request: request对象
    :rtype: HttpResponse JSON
    """
    user = request.user
    if not user.is_authenticated():
        code = "-1"
        mesg = u"系统无法自动登录"
    else:
        code = "0"
        mesg = userpackage(user)
        # mesg = u"%s 欢迎登录" % user.username
    return {"code": code, "definition": mesg}

@serialize("json")
@require_POST
def login(request):
    """
    登录处理函数
    
    :param request: request对象
    :rtype: HttpResponse JSON
    """
    mesg, code = ("", "")
    try:
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST['remember']
    except Exception, e:
        code = "-1"
        mesg = str(e)
    else:
        # print "username: %s, password: %s" % (username, password)
        # print "remember:", remember
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                djangoLogin(request, user)
                if remember:
                    # 2 weeks = 2 * 7 * 24 * 60 * 60 = 1209600
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                code = "0"
                # mesg = "User is valid, active and authenticated"
                # mesg = u"%s 欢迎登录" % user.username
                mesg = userpackage(user)
            else:
                code = "-1"
                mesg = u"账户处于未激活状态"
                # mesg = "The password is valid, but the account has been disabled!"
        else:
            code = "-1"
            mesg = u"用户名或者密码错误"
            # mesg = "The username and password were incorrect."
    finally:
        return {"code": code, "definition": mesg}

@serialize("json")
@require_POST
def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        result = {
            "code": 0,
            "definition": "success",
        }
    else:
        result = {
            "code": -1,
            "definition": str(form.errors)
        }
    return result

@serialize("json")
@require_POST
def logout(request):
    code, mesg = ("", "")
    # username = request.user.username
    try:
        djangoLogout(request)
    except Exception, e:
        code = "-1"
        # mesg = "%s 退出系统失败" % username
        mesg = "退出系统失败"
    else:
        code = "0"
        mesg = "成功退出系统"
        # mesg = "%s 成功退出系统" % username
    finally:
        return {"code": code, "definition": mesg}

@serialize("json")
def get_rooms(request):
    context = [{
      "roomId": 1,
      "roomName": "房间1",
      "plantId": 1,
      "plantName": "蘑菇",
      "time": "2013-12-25 16:41",
      "sensors": {
        "temperature": 18,
        "co2": 24,
        "humidity": 150,
      },
      "brightness": "yellow",
      "menu": {
        "data": "glyphicon-sort",
        "policy/viewer": "glyphicon-list-alt",
        "policy/setter": "glyphicon-pencil",
        "controller": "glyphicon-wrench",
      },
        
    # },
    # {
    #   "roomId": 2,
    #   "roomName": "房间2",
    #   "plantId": 2,
    #   "plantName": "蘑菇",
    #   "time": "2013-12-25 16:41",
    #   "sensors": {
    #     "temperature": 18,
    #     "co2": 24,
    #     "humidity": 150,
    #    },
    #   "brightness": "yellow",
    #     "menu": {
    #         "data": "glyphicon-sort",
    #         "policy/viewer": "glyphicon-list-alt",
    #         "policy/setter": "glyphicon-pencil",
    #         "controller": "glyphicon-wrench",
    #     },
    # },
    # {
    #   "roomId": 3,
    #   "roomName": "房间3",
    #   "plantId": 3,
    #   "plantName": "蘑菇",
    #   "time": "2013-12-25 16:41",
    #   "sensors": {
    #     "temperature": 18,
    #     "co2": 24,
    #     "humidity": 150,
    #    },
    #   "brightness": "yellow",
    #     "menu": {
    #         "data": "glyphicon-sort",
    #         "policy/viewer": "glyphicon-list-alt",
    #         "policy/setter": "glyphicon-pencil",
    #         "controller": "glyphicon-wrench",
    #     },
    }]
    return {"code": 0, "definition": "jla;jfklds", "context": context}

@serialize("json")
def get_data(request, room_id):
    data = [
        {
            "sensorId": 1,
            "sensorType": "temperature",
            "position": "上1",
            "value":
            (
                ("2014-01-08 21:08", 100),
                ("2014-01-08 21:09", 200),
                ("2014-01-08 21:15", 300),
            )
        },
        {
            "sensorId": 2,
            "sensorType": "temperature",
            "position": "上2",
            "value":
            (
                ("2014-01-08 21:08", 100),
                ("2014-01-08 21:09", 200),
                ("2014-01-08 21:15", 300),
            )
            # {
            #     "2014-01-08 21:08": 100,
            #     "2014-01-08 21:09": 200,
            #     "2014-01-08 21:15": 300,
            # }
        },
        {
            "sensorId": 3,
            "sensorType": "humidity",
            "position": "上2",
            "value":
            (
                ("2014-01-08 21:08", 100),
                ("2014-01-08 21:09", 200),
                ("2014-01-08 21:15", 300),
            )
            # {
            #     "2014-01-08 21:08": 100,
            #     "2014-01-08 21:09": 200,
            #     "2014-01-08 21:15": 300,
            # }
        },
    ]
    return {"code": 0, "data": data}

@serialize("json")
def search(request):
    get = request.GET
    room_id = get["roomId"]
    sensor_id = get["sensorId"]
    start_date = get["startDate"]
    end_date = get["endDate"]
    print room_id, sensor_id, start_date, end_date
    return {"code": 0, "data": "wait"}

@serialize("json")
@require_GET
def get_now_policy_by_room_id(request, room_id):
    print room_id
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
    return {"code": 0, "data": data}

@serialize("json")
def get_now_time_point(request, room_id):
    return {"code": 0, "nowPoint": "2014-01-07 15:00"}

@serialize("json")
def get_room_controller_list(request, room_id):
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
            "state": "on",
        },
        {
            "roomId": room_id,
            "controllerId": 4,
            "controllerType": "LED控制",
            "state": "off",
        },
        ]

    return {"code": 0, "data": data}

@serialize('json')
def get_room_controller(request, room_id, controller_id):
    return {"code": 0, "definition": "设备开启成功"}
    
@serialize("json")
def policy_list(request):
    if request.method == 'GET':
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
        return {"code":0, "data": data}
    else:
        return {"code":-1, "definition": "不是get方法"}
    
@serialize("json")
def policy_view(request, policy_id=-1):
    if request.method == 'GET':
        code = 0
        definition = "wait"
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
        return {"code": code, "policy": policy}
    elif request.method == 'POST':
        mesg = json.loads(request.POST["mesg"])
        # mesg = request.POST
        print mesg
        # print mesg["roomId"], mesg["description"]
        return {"code": 0, "definition": "添加成功"}
    else:
        return {"code":-1, "definition": "不是get方法"}


@serialize("json")
def set_policy(request):
    try:
        room_id = request.POST["roomId"]
        policy_id = request.POST["policyId"]
    except Exception, e:
        print "//////////////////////////"
        print e
        code = -1
        definition= e
    else:
        print room_id, policy_id
        code = 0
        definition = "wait"
        policy= [
            {
            "date" : "2014-01-02",
            "hour" : "09:39",
            "temperature": (100, 200),
            "humidity":  (10, 20),
            "co2":  (1, 2),
            "brightness": ["blue"],
            },
            ]
    finally:
        return {"code": code, "definition": definition, "policy": policy}
# ==========================================================


from NodeSite import settings
import socket

@serialize("json")
def config_log(request, log_type):
    address = settings.MIDDLEWARE_ADDRESS
    port = settings.MIDDLEWARE_PORT
    print address, port, log_type
    mesg = {
        "uri": "config/log/",
        "type": "request",
        "data": {
            "type": log_type,
        }
    }
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, port))
    except Exception, e:
        code = -1
        definition = "远程通信失败"
        print "Socket Error:", e
    else:
        print "connect successfully"
        mesg_str = json.dumps(mesg)
        pkg = "HEAD%sEND" % mesg_str
        print pkg
        s.send(pkg)
        s.recv(1024)
        code = 0
        definition = "发送成功"
        s.close()
    finally:
        return {"code": code, "definition": definition}


@serialize("json")
def controller_list_view(request, room_id):
    print "room_id is %s" % room_id
    code = 0
    definition = "获取列表成功"
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
            "state": "on",
        },
        {
            "roomId": room_id,
            "controllerId": 4,
            "controllerType": "LED控制",
            "state": "off",
        },
        {
            "roomId": room_id,
            "controllerId": 100,
            "controllerType": "采集频率",
            "state": 1000,
        },
        ]
    return {"code": code, "definition": definition, "context": data}

from django.http import QueryDict
@serialize("json")
def controller_view(request, controller_id):
    controller_id = int(controller_id)
    if controller_id is 100:
        try:
            params = QueryDict(request.body, request.encoding)
            freg = params["freg"]
        except Exception, e:
            print e
        else:
            print "controller_id is ", controller_id, freg            
    else:
        try:
            params = QueryDict(request.body, request.encoding)
            action = params["action"]
        except Exception, e:
            print e
        else:
            print "controller_id is ", controller_id, action
    code = 0
    definition = "控制器开启成功"
    return {"code": code, "definition": definition}

@serialize("json")
def update_name(request, key=None, ID=-1):
    if key in ["room", "plant"]:
        try:
            params = QueryDict(request.body, request.encoding)
            name = params["name"]
        except Example, e:
            print e
            definition = "修改名称失败"
            code = -1
        else:
            print key, ID, name
            definition = "成功修改名称"
            code = 0
    else:
        code = -1
        definition= "I don't know"
    return {"code": 0, "definition": definition}
    
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

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
    
# @login_required
def home(request):
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
# @login_required
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
@require_POST
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
        
    },
    {
      "roomId": 2,
      "roomName": "房间2",
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
    },
    {
      "roomId": 3,
      "roomName": "房间3",
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
    }]
    return {"code": 0, "number": len(context),"context": context}


@serialize("json")
@require_POST
def search(request):
    print request.POST
    post = request.POST
    room_id = post["roomId"]
    sensor_id = post["sensorId"]
    start_date = post["startDate"]
    end_date = post["endDate"]
    print "hello"
    print room_id, sensor_id, start_date, end_date
    return {"code": 0, "data": "wait"}

@serialize("json")
@require_GET
def get_now_policy_by_room_id(request, room_id):
    print room_id
    data = {
        "roomId": 1,
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
            "date" : "2013-12-30",
            "hour" : "20:21",
        "temperature": (100, 200),
        "humidity": (10,20),
        "co2":(1,2),
        "brightness": ["blue"],
        },
        ]
    }
    return {"code": 0, "data": data}
    
    
# ==========================================================
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

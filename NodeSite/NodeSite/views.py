# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)

from django.contrib.auth import authenticate, login as djangoLogin
# from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.models import (Group, Permission, User)

from django.contrib.contenttypes.models import ContentType

#reverse函数可以像在模板中使用url那样，在代码中使用
from django.core.urlresolvers import reverse

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
                error = '{"code": %d, "definition": %s}' % (-1, "序列化错误")
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

@serialize("json")
@require_POST
def login(request):
    """
    登录处理函数
    
    :param request: request对象
    :rtype: HttpResponse JSON
    """
    username = request.POST['username']
    password = request.POST['password']
    print "username: %s, password: %s" % (username, password)
    user = authenticate(username=username, password=password)
    mesg, code = ("", "")
    if user is not None:
        if user.is_active:
            djangoLogin(request, user)
            code = "0"
            mesg = "User is valid, active and authenticated"
        else:
            code = "-1"
            mesg = "账户处于未激活状态"
            # mesg = "The password is valid, but the account has been disabled!"
    else:
        code = "-1"
        mesg = "用户名或者密码错误"
        # mesg = "The username and password were incorrect."
    return {"code": code, "definition": mesg}

# ==========================================================
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

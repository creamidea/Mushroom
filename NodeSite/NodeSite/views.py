# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)

from django.contrib.auth import authenticate, login as djangoLogin
# from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import (Group, Permission, User)

from django.contrib.contenttypes.models import ContentType

#reverse函数可以像在模板中使用url那样，在代码中使用
from django.core.urlresolvers import reverse

# 结果序列化
def serial(func):
    pass

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

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print "username: %s, password: %s" % (username, password)
    user = authenticate(username=username, password=password)
    mesg = ""
    if user is not None:
        if user.is_active:
            djangoLogin(request, user)
            
            mesg = "User is valid, active and authenticated"
        else:
            mesg = "The password is valid, but the account has been disabled!"
    else:
        mesg = "The username and password were incorrect."
    return HttpResponse(mesg)

# ==========================================================
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

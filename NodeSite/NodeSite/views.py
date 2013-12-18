# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import (Group, Permission, User)

from django.contrib.contenttypes.models import ContentType

#reverse函数可以像在模板中使用url那样，在代码中使用
from django.core.urlresolvers import reverse

# @login_required
def home(request):
    """
    主页视图处理函数
    
    :param request: request对象
    :rtype: HttpResponse
    """
    return render(request, 'index.html')

# ==========================================================
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

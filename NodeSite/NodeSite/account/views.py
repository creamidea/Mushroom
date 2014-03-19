# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.contrib.auth.decorators import (login_required,
                                            permission_required)

from django.contrib.auth.models import (Permission, Group, User)

from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse   #reverse函数可以像在模板中使用url那样，在代码中使用

from ..decorators import json_response

@json_response
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # request.is_ajax()
        if form.is_valid():
            auth_login(request, form.get_user())
            return dict(body="login successfully")
    else:
         return dict(body="login fail, please go to the index.")
             # HttpResponseRedirect(redirect_to="/")
             # login(request, template_name='signin.html')

def signout(request):
    return logout(request, next_page=reverse('home'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # import inspect, sys
        # frame = inspect.stack()[1][0]
        # caller__name__ = frame.f_locals['__name__']
        # print(caller__name__)

        if form.is_valid():
            content_type = ContentType.objects.get(app_label='account', model='user')
            # p, created = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)
            p = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)
            new_user = form.save()
            new_user.user_permissions.add(p)
            return HttpResponseRedirect(reverse('singin'))
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {
        'form': form,
    })

@login_required
def profile(request):
    print '/////////////////////////////////'
    if request.user.has_perm('auth.can_vote'):
        print 'you can vote'
    form = UserCreationForm()
    print dir(request.user.groups)
    # print request.user.get_all_permissions()
    return render(request, 'profile.html', {
        'form': form,
    })

@permission_required('auth.can_manage_users', raise_exception=True)
def manage(request):
    
    form = UserCreationForm()
    return render(request, 'manage.html', {
        'form': form,
    })

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (Group, Permission, User)

from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse   #reverse函数可以像在模板中使用url那样，在代码中使用

@login_required
def home(request):
    return render(request, 'index.html')

def signin(request):
    return login(request, template_name = 'accounts/signin.html')

def signout(request):
    return logout(request, next_page = reverse('home'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # import inspect, sys
        # frame = inspect.stack()[1][0]
        # caller__name__ = frame.f_locals['__name__']
        # print(caller__name__)

        if form.is_valid():
            # content_type = ContentType.objects.get(app_label='auth', model='user')
            # p, created = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)
            p = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)
            new_user = form.save()
            new_user.user_permissions.add(p)
            return HttpResponseRedirect(reverse('singin'))
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {
        'form': form,
    })

@login_required
def profile(request):
    print '/////////////////////////////////'
    if request.user.has_perm('auth.can_vote'):
        print 'you can vote'
    form = UserCreationForm()
    print request.user.get_all_permissions()
    return render(request, 'accounts/profile.html', {
            'form': form,
    })

@login_required
def settings(request):
    form = UserCreationForm()
    print request.user.get_all_permissions()
    return render(request, 'mushroom/settings.html', {
        'form': form,
    })

# ==========================================================
# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

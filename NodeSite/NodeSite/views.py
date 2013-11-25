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

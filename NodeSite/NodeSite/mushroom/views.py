# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (Group, Permission, User)

from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse

# Create your views here.
@login_required
def settings(request):
    form = UserCreationForm()
    print request.user.get_all_permissions()
    return render(request, 'settings.html', {
        'form': form,
    })


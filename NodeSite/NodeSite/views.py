# -*- coding: utf-8 -*-
#reverse函数可以像在模板中使用url那样，在代码中使用
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
# from django.contrib.auth.views import (login, logout)
from django.contrib.auth.models import (Group, Permission, User)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

def home(request):
    title = u"蘑菇房监控平台"
    if not request.user.is_authenticated():
        return render(request,"signin.html", dict(title=title))
    else:
        return render(request,"index.html", dict(title=title))

# test
def create_playlist(request):
    print request.user.get_all_permissions()
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully')
    return render(request, "playlists/create.html")

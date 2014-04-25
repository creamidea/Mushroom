# -*- coding: utf-8 -*-

# Create your views here.
#reverse函数可以像在模板中使用url那样，在代码中使用
import json
import re
from django.core.urlresolvers import reverse
# from django.core import serializers
from django.template import RequestContext
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.http import (HttpResponse, HttpResponseRedirect, QueryDict, Http404)
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (login, logout)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import (login_required, permission_required)
from django.contrib.auth.models import (Permission, Group, User)
from django.contrib.contenttypes.models import ContentType
from ..decorators import json_response
from forms import MushroomUserCreationFrom
from models import MushroomUser

# @json_response
def signin(request):
    if request.method == 'POST':
        check = request.POST.get('remember', None)
        if check == 'on':
            # 2 weeks = 1209600 seconds
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)
    return login(request, 'signin.html')
    # return login(request, 'signin.html', extra_context=RequestContext(request))

        # form = AuthenticationForm(data=request.POST)
        # # request.is_ajax()
        # if form.is_valid():
        #     auth_login(request, form.get_user())
        #     # return dict(body="login successfully")
        #     return HttpResponseRedirect(redirect_to=reverse('home'))
    # return login(request, template_name='signin.html', )

def signout(request):
    return logout(request, next_page=reverse('signin'))

def signup(request):
    user = request.user
    if request.method == 'POST':
        form = MushroomUserCreationFrom(request.POST)
        # import inspect, sys
        # frame = inspect.stack()[1][0]
        # caller__name__ = frame.f_locals['__name__']
        # print(caller__name__)

        if form.is_valid():
            new_user = form.save()
            # return HttpResponse(u"创建成功")
            return HttpResponseRedirect(reverse("manage"))

    else:
        form = MushroomUserCreationFrom()
    return render(request, "signup.html", {
        'form': form,
    })

@login_required
def profile(request):
    # print '/////////////////////////////////'
    # if request.user.has_perm('auth.can_vote'):
    #     print 'you can vote'
    form = MushroomUserCreationFrom()
    # print request.user.groups.values_list()
    # print dir(request.user)
    user = request.user
    [username, email] = [user.username, user.email]
    # phone = None
    phone = user.phone
    # print request.user.get_all_permissions()
    return render(request, 'profile.html', {
        'passwordChangeForm': PasswordChangeForm(user=user),
        'form': form,
        'username': username,
        'email': email,
        'phone': phone,
    })

# @permission_required('auth.can_manage_users', raise_exception=True)
def manage(request):
    # if request
    # print request.user.get_profile()
    creation_form = MushroomUserCreationFrom()
    users = MushroomUser.objects.all()
    # print users
    return render(request, 'manage.html', {
        'creation_form': creation_form,
        'users': users
    })

# @json_response
# @sensitive_post_parameters()
@csrf_protect
@require_POST
@login_required
def password_change(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    wrapper_html = '''
        <div class="alert %s alert-dismissable">
          <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
          <strong>%s</strong>
        </div>'''

    alert_html = ""
    if form.is_valid():
        form.save()
        data = wrapper_html % ("alert-success", u"密码修改成功")
    else:
        data = wrapper_html % ("alert-danger", form.errors.as_ul())
        # data = u"创建失败"
        # data = "failed"
        # print type(form.errors), dir(form.errors)
    # print ">>> ", data
    if request.is_ajax():
        pkg =  {"body":data}
        # print pkg
        data = json.dumps(pkg)
    return HttpResponse(data, content_type="application/json")
    # print "old_password: ", request.POST.get("old_password")
    # return HttpResponse({"body":"hello"})
    # return HttpResponse("elldasf")


@login_required
def password_change_done(request):
    return HttpResponse(u"密码修改成功")

# def add_message
@json_response
def profile_change(request):
    PUT = QueryDict(request.body)
    phone = PUT.get('phone', None)
    email = PUT.get('email', None)
    uid = PUT.get('uid', None)
    if uid is None: raise Http404()
    code = 0
    body = u"修改成功"
    user = MushroomUser.objects.get(pk=uid)
    if phone is not None:
        old_phone = user.phone
        if phone != old_phone:
            if re.match('^\d{11}$', phone):
                code = 0
                user.phone = phone
                user.save()
            else:
                code = -1
                body = u"请输入11位有效的电话号码。"
    if email is not None:
        old_email = user.email
        if email != old_email:
            if re.match('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$', email, re.I):
                code = 0
                user.email = email
                user.save()
            else:
                body = u"请输入有效的电子邮件。"
                code = -1
    return dict(code=code, body=body)
    
@json_response
def account_delete(request):
    DELETE = QueryDict(request.body)
    try:
        uid = DELETE['uid']
        user = MushroomUser.objects.get(pk=uid)
        user.delete()
    except Exception, e:
        # print e
        body = e
        code = -1
    else:
        body = uid
        code = 0
    finally:
        return dict(code=code, body=body)

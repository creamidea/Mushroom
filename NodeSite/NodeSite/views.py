# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'index.html')

def signin(request):
    return login(request, template_name = 'registration/signin.html')

def signout(request):
    return logout(request, next_page = '/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/signin/")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {
        'form': form,
    })

def profile(request):
    return render(request, 'profile.html')



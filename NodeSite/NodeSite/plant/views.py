# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello, world")

def list(request):
    return HttpResponse("Here is plant list")

def plant(request, plant_id):
    title = u"植物%s信息" % plant_id
    return render(request,
                      "plant-item.html",
                      dict(
                          title=title,
                          plant_id=plant_id,
                      ),
    )
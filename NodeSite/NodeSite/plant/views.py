# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.views.decorators.http import  require_POST
from django.contrib.auth.decorators import login_required
from ..decorators import json_response
from NodeSite.db.db_operator import DbOperator

@login_required
def hello(request):
    return HttpResponse("Hello, world")

@login_required
def list(request):
    return HttpResponse("Here is plant list")

@login_required
def plant(request, plant_id):
    if request.method == 'GET':
        if request.is_ajax:
            pass
        else:
            title = u"植物%s信息" % plant_id
            return render(request,
                          "plant-item.html",
                        dict(title=title,plant_id=plant_id,),
                    )
    if request.method == 'DELETE':
        DELETE = QueryDict(request.body)
        try:
            plant_name = DELETE['plantName']
        except KeyError, e:
            return HttpResponse(str(e))
        else:
            return ajax_delete_plant(request, plant_name)

@json_response
@login_required
def ajax_delete_plant(request, plant_name):
    db = DbOperator()
    (code, mesg) = db.delete_plant(plant_name)
    return dict(code=code, body=mesg)

@json_response
@login_required
def plant_name(request, plant_id):
    if request.method == "PUT":
        PUT = QueryDict(request.body)
        try:
            new_name = PUT['name']
        except KeyError, e:
            return HttpResponse(str(e))
        else:
            db = DbOperator()
            (code, mesg) = db.update_plant(plant_id, new_name)
            return dict(code=code, body=mesg)
    
@json_response
@login_required
def get_plant_name_list(request):
    db = DbOperator()
    name_list = db.plant_dict
    # print name_list.next()
    count = 0
    result = {}
    for key, val in name_list.iteritems():
        result[val.plant_id] = val.plant_name.strip()
    # print result
    return dict(code=0, body=result)

# -*- coding: utf-8 -*-
# Create your views here.

# import sys
# print sys.getdefaultencoding()
from django.http import QueryDict
from django.http import HttpResponse
from django.views.decorators.http import  require_POST
from ..decorators import json_response
from NodeSite.db import db_operator as db
# from NodeSite.db.db_operator import db_inst as db

def hello(request):
    return HttpResponse("Hello, world")

@json_response
def list(request):
    data = db.all_policy_info()
    return dict(body=data)

@json_response
def now(request, room_id):
    data = None
    if request.method == 'GET':
        # 获取指定房间正在被执行的策略
        data = db.current_policy(room_id)
        # print room_id, data

    elif request.method == 'PUT':
        # 修改正在执行中的策略
        data = "Update policy successfully"
    return dict(body=data)

@json_response
@require_POST
def create(request):
    # 增加策略
    post = request.POST
    room_id = post.get("roomId")
    description = post.get("description")
    policys = post.get("policys")
    print room_id, policys
    code = db.new_policy_instance(room_id=room_id, description=description, policy=policys)
    if code is 0:
        data = "Create Successfully!"
    else:
        data = "创建失败，请稍候再试。"
    return dict(body=data)

@json_response
def policy(request, policy_id):
    # 获取策略详细内容，通过策略号
    if request.method == 'GET':
        # 获取策略信息
        data = db.get_policy(policy_id)


    elif request.method == 'DELETE':
        # 删除策略
        data = "Delete successfully!"

    return dict(body=data)

@json_response
def description(request, policy_id=None):
    # 获取策略的描述
    data = None
    if request.method == 'POST':
        data = "Create Successfully"
    elif request.method == 'PUT':
        # Update the description
        put = QueryDict(request.body)
        description = put.get('description')
        code = db.update_policy_desc(policy_id, description)
        if code is 0:
            data = "Update Successfully, description:", description
        else:
            data = "创建失败，请稍候再试！"

    elif request.method == 'GET':        # Get the description
        data = "You will get the policy %s description" % policy_id
    return dict(body=data)

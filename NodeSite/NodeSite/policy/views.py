# -*- coding: utf-8 -*-
# Create your views here.

# import sys
# print sys.getdefaultencoding()
import json
import datetime
import re
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.views.decorators.http import  require_POST
from django.contrib.sites.models import RequestSite
from django.contrib.auth.decorators import login_required
from ..decorators import json_response
from NodeSite.db.db_operator import DbOperator
from NodeSite.settings import MEDIA_ROOT, UPLOAD_PATH_PREFIX
from models import OutputStatistics

db = DbOperator()
image_format = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
}

def hello(request):
    return HttpResponse("Hello, world")

@login_required
def policy_list(request):
    if request.is_ajax():
        return ajax_list(request)
    else:
        return render(request, 'policy-list.html',
                      {'title': u"策略"})
@json_response
@login_required
def ajax_list(request):
    data = db.all_policy_info()
    return dict(body=data)

@json_response
@login_required
def policy_room_list(request, room_id):
    db = DbOperator()
    data = db.get_room_policy(room_id)
    # print ">>>>", data
    return dict(body=data)

@login_required
def now(request, room_id):
    if request.is_ajax():
        return ajax_now(request, room_id)
    else:
        return render(request, 'policy-now.html',
                      {'title': '正在执行的策略'})
@json_response
@login_required
def ajax_now(request, room_id):
    data = None
    code = None
    room_id = int(room_id)
    if request.method == 'GET':
        # 获取指定房间正在被执行的策略
        db = DbOperator()
        # data = db.current_policy(int(room_id))
        (code, data) = db.get_policy_instance_now(room_id=int(room_id))
        # print room_id, data
    elif request.method == 'PUT':
        # 修改正在执行中的策略
        code = 0
        data = u"修改真在执行的策略成功"
    return dict(code=0, body=data)

@json_response
@login_required
def ajax_now_by_policy_id(request, policy_id):
    # print policy_id, "\\\\\\\\\\\\\\\\\\\\\\\\"
    try:
        # code = None
        # data = None
        policy_id = int(policy_id)
    except ValueError, e:
        code = -1
        data = str(e)
    else:
        db = DbOperator()
        (code, data) = db.get_policy_instance_now(policy_id=policy_id)
    finally:
        return dict(code=code, body=data)

@login_required
def create(request):
    if request.method == 'GET':
        # 这个用于渲染页面
        room_id = request.GET.get('roomId', "")
        return render(request, 'policy-create.html',
                      {'room_id':room_id})
    elif request.method == 'POST':
        return ajax_create(request)
        
@json_response
@login_required
def ajax_create(request):
    # 增加策略
    post = request.POST
    # room_id = int(post.get("roomId"))
    description = post.get("description")
    rules = post.get("rules")
    # start_date = post.get("startDate")
    # start_time = post.get("startTime")
    # startAt = "%s %s" % (start_date, start_time)
    # policy = json.loads(post.get("policy"))
    if len(rules) is 0:
        return dict(code=-1, body=u"策略为空")
    rules = json.loads(rules)
    # print description, rules
    # print room_id, description, start_date, start_time, policy
    db = DbOperator()
    # code = db.new_policy_instance(dict(roomId=room_id, description=description, policy=policy, plantName="test", startAt=startAt))
    (code, mesg) = db.new_policy(description, rules)
    return dict(code=code, body=mesg)

@json_response
def get_plan_list(request, policy_id):
    db = DbOperator()
    try:
        policy_id = int(policy_id)
        (code, data) = db.get_policy_instance_plan_list(policy_id)
    except Exception, e:
        code = -1
        data = str(e)
    return dict(code=code, body=data)

@json_response
@login_required
def get_done_list(request, policy_id):
    try:
        policy_id = int(policy_id)
        db = DbOperator()
        (code, data) = db.get_policy_instance_done_list(policy_id)
    except Exception, e:
        code = -1
        data = str(e)
        return dict(code=code, body=data)
    result = []
    for item in data:
        policyInstanceId = item["policyInstanceId"]
        outputstatistics = OutputStatistics.objects.filter(policy_instance_id=policyInstanceId)
        # 为何这里这样写会报错
        # outputstatistics.values()[0]说越界呢？
        ops = outputstatistics.values()
        (output, image) = (None, None)
        for i in ops:
            output = i.get("output")
            image = i.get("image")
        result.append({
            "policyInstanceId": policyInstanceId,
            "roomDesc": item["roomDesc"],
            "plantName": item["plantName"],
            "startAt": item["startAt"],
            "output": output,
            "image": image,
        })
    return dict(code=0, body=result)

@login_required
def policy(request, policy_id):
    # 获取策略详细内容，通过策略号
    policy_id = int(policy_id)
    if request.method == 'GET':
        # 获取策略信息
        if request.is_ajax():
            return ajax_get_policy(request, policy_id)
        else:
            title = u"策略%s" % policy_id
            # outputstatistics = OutputStatistics.objects.filter(policy_id=policy_id)
            # print outputstatistics.values(), dir(outputstatistics)
            return render(request, "policy-item.html",
                          {'title': title, 'policy_id': policy_id,
                           # 'values': outputstatistics.values(),
                          })

    elif request.method == 'DELETE':
        # 删除策略
        return ajax_delete_policy(request, policy_id)

@json_response
@login_required
def ajax_get_policy(request, policy_id):
    data = db.get_policy(policy_id)
    # print "AJAX GET POLICY:", data
    return dict(body=data)

@json_response
@login_required
def ajax_delete_policy(request, policy_id):
    db = DbOperator()
    result = db.delete_policy(policy_id)
    if result['code'] is 0:
        code = 0
        data = u"删除成功!"
    else:
        code = -1
        data = result['definition']
    return dict(code=code, body=data)

@json_response
@login_required
def description(request, policy_id=None):
    print policy_id, "///////////////////////////"
    # 获取策略的描述
    data = None
    if request.method == 'POST':
        data = "Create Successfully"
    elif request.method == 'PUT':
        # Update the description
        put = QueryDict(request.body)
        description = put.get('description')
        result = db.update_policy_desc(int(policy_id), description)
        if result["code"] is 0:
            data = "修改成功，新的描述为：", description
            code = 0
        else:
            code = -1
            data = "创建失败，请稍候再试！"

    elif request.method == 'GET':        # Get the description
        data = "You will get the policy %s description" % policy_id
    return dict(code=code, body=data)

@json_response
@login_required
@require_POST
def policy_instance_output_save(request, piid):
    print piid
    output = request.POST.get("output")
    print output
    try:
        record = OutputStatistics.objects.filter(policy_instance_id=piid)
        print record, dir(record)
        if len(record) is 0:
            # 说明这是一条新纪录
            OutputStatistics(policy_instance_id=piid, output=output).save()
        else:
            record.update(output=output)
        code = 0
        body = None
    except Exception, e:
        code = -1
        body = e
        print e
    finally:
        return dict(code=code, body=body)
    
@login_required
@require_POST
def policy_instance_image_save(request, piid):
    POST = request.POST
    policy_instance_id = piid
    pre_url = POST.get('pre_url')
    back = '''<a href="%s">%s</a>''' % (pre_url, u"返回")
    message = None
    image = request.FILES['image']
    try:
        image = request.FILES['image']
    except KeyError, e:
        message = u"没有上传有效文件！%s" % back
        return HttpResponse(message)
    else:
        # print image.content_type
        # TODO: 这里是以时间作为文件的名称的，
        # 估计以后遇到频繁上传时最好使用MD5之类的HASH方法。
        image_prefix = UPLOAD_PATH_PREFIX+'/static/upload/'
        image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        message = u"未知错误。 %s" % back
        try:
            image_affix = image_format[image.content_type]
        except KeyError, e:
            message = u'不支持该文件格式!%s' % back
            return HttpResponse(message)
    
        pathname = image_prefix+image_name+image_affix
        with open(pathname, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        
        try:
            record = OutputStatistics.objects.filter(policy_instance_id=piid)
            print record, dir(record)
            if len(record) is 0:
                # 说明这是一条新纪录
                OutputStatistics(
                    policy_instance_id=piid,
                    image=re.match('^%s(.*)'%UPLOAD_PATH_PREFIX, pathname).groups()[0]).save()
            else:
                record.update(image=re.match('^%s(.*)'%UPLOAD_PATH_PREFIX, pathname).groups()[0])
        except Exception, e:
            # print e
            message = u"存入错误。%s" % back
            return HttpResponse(message)
        else:
            message = u"创建成功，正在跳转。"
            return HttpResponseRedirect(pre_url)

@login_required
def save_output(request):
    POST = request.POST
    policy_id = POST.get('policy_id')
    output = POST.get('output', None)
    
    pre_url = POST.get('pre_url')
    back = '''<a href="%s">%s</a>''' % (pre_url, u"返回")
    
    if not output: return HttpResponse(u"请输入有效的产量值%s" % back)
    try:
        image = request.FILES['image']
    except KeyError, e:
        message = u"没有上传有效文件！%s" % back
        return HttpResponse(message)

    else:
        # print image.content_type
        # TODO: 这里是以时间作为文件的名称的，
        # 估计以后遇到频繁上传时最好使用MD5之类的HASH方法。
        image_prefix = 'NodeSite/static/upload/'
        image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        message = u"未知错误。 %s" % back
        try:
            image_affix = image_format[image.content_type]
        except KeyError, e:
            message = u'不支持该文件格式!%s' % back
            return HttpResponse(message)
    
        # print policy_id, output
        
        pathname = image_prefix+image_name+image_affix
        with open(pathname, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        try:
            outputstatistics = OutputStatistics(
                policy_id = int(policy_id),
                start_time = datetime.datetime.now(),
                output = float(output),
                image = re.match('^NodeSite(.*)', pathname).groups()[0])
        except Exception, e:
            # print e
            message = u"存入错误。%s" % back
            return HttpResponse(message)
        else:
            outputstatistics.save()
            message = u"创建成功，正在跳转。"
            return HttpResponseRedirect('/policy/%s/' % policy_id)
        
@login_required
def delete_output(request):
    delete = QueryDict(request.body)
    output_id = delete.get('outputId')
    try:
        OutputStatistics.objects.filter(id=output_id).delete()
    except Exception, e:
        message = u"删除失败"
    else:
        message = u'删除成功'
    finally:
        return HttpResponse(message)

# 策略实例处理的地方
@json_response
@require_POST
@login_required
def create_policy_instance(request):
    POST = request.POST
    try:
        policy_id = int(POST["pid"])
        roomDesc = POST["roomDesc"]
        plantName = POST["plantName"]
        startDate = POST["startDate"]
        startTime = POST["startTime"]
        startAt = "%s %s" % (startDate, startTime)
    except KeyError, e:
        code = -1
        mesg = e
    else:
        db = DbOperator()
        # print ".asdjfklsadjf..............", policy_id, plantName, roomDesc, startAt
        (code, mesg) = db.new_policy_instance(policy_id, plantName, roomDesc, startAt)
    finally:
        if code is -1:
            mesg = u"创建失败"
        return dict(code=code, body=mesg)

@login_required
def policy_instance(request, piid):
    if request.method == 'DELETE':
        return ajax_policy_instance_delete(request, piid)
    elif request.method == 'PUT':
        return ajax_policy_instance_update(request, piid)

@json_response
def ajax_policy_instance_delete(request, piid):
    db = DbOperator()
    result = db.delete_policy_instance(int(piid))
    if result is 0:
        return dict(code=0, body=u"删除成功")
    else:
        return dict(body=u"删除失败")
    
@json_response
def ajax_policy_instance_update(request, piid):
    db = DbOperator()
    PUT = QueryDict(request.body)
    roomDesc = PUT.get("roomDesc")
    plantName = PUT.get("plantName")
    startAt = PUT.get("startAt")
    print roomDesc, plantName, startAt
    (code, result) = db.update_policy_instance(piid, roomDesc, plantName, startAt)
    if code is -1:
        result = u"修改失败"
    return dict(code=code, body=result)

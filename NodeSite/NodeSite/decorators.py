# -*- coding: utf-8 -*-

from functools import wraps
# from decorator import decorator
import json

from django.http import HttpResponse

def serialize(target="json"):
    """使用装饰器序列化参数"""
    _serialize = {
        "json": json.dumps,
    }
    def wrapper1(func):
        @wraps(func)
        def wrapper2(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                response = HttpResponse(_serialize[target](result))
            except:
                error = '{"code": %d, "definition": %s}' % (-1, u"序列化错误")
                response = HttpResponse(error)
            return response
        return wrapper2
    return wrapper1


def json_response(func):
    "使用装饰器返回json格式的回应包"
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            result = json.dumps(result)
        except:
            result = '{"code": %d, "definition": %s}' % (-1, u"序列化错误")
        # 将头部设置成json格式，那么jQuery接受到之后就会自动序列化成json对象。
        return HttpResponse(result, content_type="application/json")
    return wrapper

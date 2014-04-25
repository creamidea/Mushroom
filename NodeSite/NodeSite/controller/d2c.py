# -*- coding: utf-8 -*-

import json
import socket
import gevent
from hashlib import md5
from binascii import a2b_hex, b2a_hex

HEAD = "MUSHROOM"
HEAD_BIT = 8
VER = 1
VER_BIT = 1
VERSION = '{:{fill}{width}{base}}'.format(VER, fill='0', width=2*VER_BIT, base ='x')
LEN_BIT = 4

# MUSHROOM(8)VERSION(1)Length(4)Body(JSON SERIALIZE)
def get_body_length(str_body=None):
    # 获取消息体body长度
    # :param str_body
    # rtype: int
    if not str_body or not isinstance(str_body, basestring):
    # 排除空值或者不是字符串的情况
        return 0
    return len(str_body)

def encode_body(json_body=None):
    # 将json编码成字符串
    result = None
    try:
        result = json.dumps(json_body)
    except Exception, e:
        result = str(e)
    finally:
        return result
    
def decode_body(str_body=None):
    print "[decode body]", str_body
    # 将字符串解码成json
    result = None
    try:
        result = json.loads(str_body)
    except Exception, e:
        result = str(e)
    finally:
        return result
    
def pack(json_body=None):
    # 将数据打包成协议指定格式
    # :param json_body 需要打包的数据
    if not isinstance(json_body, basestring):
        s_body = encode_body(json_body)
    else:
        s_body = json_body
    length = get_body_length(s_body)
    s_len = '{:{fill}{width}{base}}'.format(length, fill='0', width=2*LEN_BIT, base='x')
    # print "[PACK]: ", s_len
    result = "%s%s%s%s" % (HEAD, str(a2b_hex(VERSION)), str(a2b_hex(s_len)), s_body)
    return result

def unpack(fd):
    # 拆包
    # 这里是解析的主体，需要传入一个fd，就是数据源。
    if isinstance(fd, file):
        read = fd.read
        # fd.seek(0)              # 许要将文件指针指向第一个，不知为何直接使用read()，会读取第二个字符，而不是第一个
    elif isinstance(fd, socket._socketobject) or \
      isinstance(fd, gevent.socket.socket):
        read = fd.recv
    else:
        print "unknow fd: %s" % str(type(fd))
        return None

    # print "start unpack..."
    version = body = length = None
    # print "start reading..."
    # TODO:这里的read在gevent模式下会出现问题：This operation would block foreverxs
    try:
    # if True:
        readed = read(1)
        # print readed
        if readed == HEAD[0]:
            readed += read(2)
            if readed == HEAD[:3]:
                readed += read(HEAD_BIT - 3)
                # print readed
                if readed == HEAD:
                    version = int(b2a_hex(read(VER_BIT)), 16)
                    length = int(b2a_hex(read(LEN_BIT)), 16)
                    body = read(length)
                    # print ">>>", version, length, body
    except Exception, e:
        print ">>>> e:", e

    # 返回的body没有被json反序列化
    return (body, version, length)

# ################################
# 签名
def sign(data):
    return md5_str(data)

# ################################
# 帮助包
def md5_str(data):
    if isinstance(data, str):
        return md5.update(data).digest()
    else:
        return ""

# #################################
# 构造一些常用的命令包
def make_controller_package(cid=None, action=None):
    # TODO: 需要取出ROOMID，根据controller id就可以全局唯一确定一台设备
    if cid == None or action == None: return None
    json_body = {
        "uri": "device/controller",
        "type": "request",   
        "data": {
            "roomId": None,
            "controllerId": cid,
            "action": action,
        }
    }
    r = pack(json_body)
    return r

    
# ##########TEST###################
if __name__ == "__main__":
    print "Test Starting..."
    
    json_body = {
        "uri": "device/controller",
        "type": "request",   
        "data": {                    
            "roomId": "1",
            "controllerId": "1",
            "action": "on",
        }
    }
        
    r = pack(json_body)
    print r, type(r)
    
    with open('data.txt', 'w') as f:
        f.write(r)
        
    with open('data.txt', 'r') as f:
        body, version, length = unpack(f)
        print body, version, length
        msg = decode_body(body)
        print msg
        print msg["uri"], msg["type"], msg["data"]["roomId"]
    
    # HOST = '127.0.0.1'    # The remote host
    # PORT = 50007              # The same port as used by the server
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print type(s)
    # print isinstance(s, socket._socketobject)
    # s.connect((HOST, PORT))
    # unpack(s)
    # s.sendall('Hello, world')
    # data = s.recv(1024)
    # s.close()
    # print 'Received', repr(data)

# -*- coding: utf-8 -*-
import threading
# import sched, time
from threading import Timer
import sched, time

# TODO:感觉这里使用普通的socket就可以了，毕竟不涉及多个套接字
# 建立的链路只有一个，这边是客户端。不过可以使用select来做查询
# 不知道是否还会在写的时候阻塞
import socket
import gevent
from gevent import socket as gsocket
from gevent.event import Event
    
from d2c import pack, unpack, make_controller_package, sign, encode_body

reconnect_time = 2                 # 60s重新连接

# #################################
class Communicate(object):
    """
    通信类
    """
    def __init__(self, address=("10.18.50.66", "9001")):
        """
        初始化必要信息
        """
        self.address = address
        # 连接句柄
        self.handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.handler.setblocking(0)
        self.is_connect = False #标志是否处于连通状态，在connect函数中为true，在close函数中为false
        self.jobs = []          # 这个是工作表
    def connect(self):
        """
        连接函数
        """
        try:
            self.handler.connect(self.address)
            print "=" * 60
            print "[Communicate Successful]Address:%s, Port: %s" % (self.address)
            print "=" * 60
        except Exception, e:
            print "=" * 60
            print "[Communicate Error: connect]", e
            print "=" * 60
            self.reconnect()
        else:
            self.is_connect = True
    def close(self):
        """
        关闭连接
        """
        if self.handler:
            self.handler.close()
            self.is_connect = False
    def reconnect(self):
        """
        重新开始连接，用于断开，或者一开始没有连接成功
        """
        self.close()
        self.handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Timer(reconnect_time, self.connect, ())
        
    def send(self, pkg=None):
        if self.is_connect is False: return "远程服务器未打开。"
        # if self.is_connect is False: return "The Communication Server is not connection."
        print "start sending..."
        totalsent = 0
        MSGLEN = len(pkg)
        while totalsent < MSGLEN:
            try:
                sent = self.handler.send(pkg[totalsent:])
            except socket.error, e:
                print "[Communicate Error: send]: ", e
                # self.reconnect()
                return -1       # 直接返回
            else:
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
    
    def receive(self, socket=None):
        # 接受函数，拆包并将其通知出去
        # if self.is_connect is False: return "The Communication Server is not connection."
        if self.is_connect is False: return "远程服务器未打开。"
        return unpack(socket)

    def send_and_receive(self, cid=None, action=None):
        """
        # 发送并接受包
        # 返回拆开的包
        """
        if self.is_connect is False:
            self.reconnect()
            return "连接远程服务器失败，正在重新连接。"
        # if self.is_connect is False: return "The Communication Server is not connection."

        print "send and receive", cid, action
        pkg = make_controller_package(cid, action)
        print pkg
        # TODO: 这里需要经一步安全的发送数据
        try:
            print "[communicat send_and_receive]"
            self.send(pkg)
        except RuntimeError, e:
            print "[Communicate Error: send_and_receive]:", e
            # TODO:暂时直接返回
            return {code: -1, error: e}
        
            # TODO:这里可能需要稍微变一下，不知道在处理并发的时候会不出现异常
            # self.reconnect()
            # self.event.wait()
            # send_and_receive(cid, action)
        else:
            # 返回解析好的数据包(body, version, length)
            # pass
            # with open('Nodesite/controller/data.txt', 'r') as f:
            #     return unpack(f)
            try:
                data = unpack(self.handler)
            except Exception, e:
                return {code: -1, error: e}
            else:
                return data
            



class SyncService(object):
    """
    # 同步服务
    """
    # 这个用于存储所有控制器的状态
    # 这里可能使得房间与设备绑定了，后期可能会遇到一些问题
    # 但是在我现在看来，应该这里没有问题
    # {[:roomId]: ([signature], [notice object/channel])}
    # rooms = {
    #   [:roomId]: ([:signature], [gevent.Event()])
    # }
    rooms = {}
    json_body = {
        "uri": "device/controller/sync",
        "type": "request",
    }
    def __init__(self, address=("10.18.50.66", "9001"), interval=60):
        """
        创建连接句柄
        """
        # 这个信道用于和中间件进行同步
        print "[Sync Service]:", address, interval
        self.address = address
        self.handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connect = False
        self.package = pack(self.json_body)
        # 同步参数
        self.interval = interval
        self.sync_timer = None
        
        self.connect()          # 自启动
        

    def connect(self):
        try:
            # self.handler.settimeout(0)
            self.handler.connect(self.address)
            print "=" * 60
            print "[Sync Successful]Address:%s, Port: %s" % (self.address)
            print "=" * 60
        except Exception, e:
            print "=" * 60
            print "[Sync Error: connect]", e
            print "=" * 60
            self.reconnect()
        else:
            self.is_connect = True
    def close(self):
        """
        关闭连接
        """
        if self.handler:
            self.handler.close()
            self.is_connect = False
    def reconnect(self):
        """
        重新开始连接，用于断开，或者一开始没有连接成功
        """
        self.close()
        self.handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.handler.setblocking(0)
        Timer(reconnect_time, self.connect, ())
        
    def update(self, room_id):
        """
        # 更新函数，用于返回request请求
        # 其实这里也是对外地接口
        """
        print "here is update"
        # 获取唤醒时从哪里获得的
        data = room[room_id][1].get()
        return data

    def __send(self):
        """
        # 发送同步请求
        """
        if self.is_connect is False: return "The Sync Server is not connection."
        pkg = self.package
        if pkg is None: return
        totalsent = 0
        MSGLEN = len(pkg)
        while totalsent < MSGLEN:
            try:
                sent = self.handler.send(pkg[totalsent:])
            except socket.error, e:
                print "[Sync Error: __send]: ", e
                # self.reconnect()
                return -1         # 返回异常
            else:
                print "send: ", sent
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
        print "[sync __send]:", pkg
        
        self.__receive()        # 开始接受信息

    def __receive(self):
        """
        # 接收函数，并进行拆包
        """
        if self.is_connect is False: return "The Sync Server is not connection."
        # 从缓冲区读取数据
        body, version, length = unpack(self.handler)
        if body is None: return
        # 对body进行序列化
        msg = encode_body(body)
        print "[Sync: __receive]"
        print msg, body
        print "-" * 30
        data = msg.get("data", None)
        if data is None: return
        signature = sign(data)  # 数据签名
        room_id = data.get("roomId", None)
        if room_id is None: return
        try:
            old_signature = self.rooms[room_id][0]
            if old_signature != signature:
                # 如果数据区的签名不同，则说明控制器状态发生变化，则唤醒wait()，将data传过去 
                room[room_id][1].set(data)
        except KeyError:
            # 如果发生KeyError，则说明这个房间是新的，则存入
            event = Event()
            self.rooms[room_id] = (signature, event)
            event.set(data)

    def __sync(self):
        if self.is_connect is False: return "The Sync Server is not connection."
        print "[sync] syncing..."
        self.__send()
        # self.__receive()
        # 定时发送同步请求
        self.sync_timer = Timer(self.interval, self.__sync, ())
        self.sync_timer.start()
    
    def start(self):
        """
        # 用于处理和服务器同步的函数
        """
        print "[Sync] start.sync..."
        self.__sync()

    def stop(self):
        """
        # 用于暂停同步函数
        """
        print "[Sync]stop sync..."
        if self.sync_timer:
            self.sync_timer.cancel()

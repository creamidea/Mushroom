# -*- coding: utf-8 -*-
import threading
# import sched, time
from threading import Timer

import socket
from gevent.event import Event
    
from d2c import pack, unpack, make_controller_package, sign

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

        # print ">>>", str(type(self.handler))
    def connect(self):
        """
        连接函数
        """
        try:
            self.handler.connect(self.address)
        except Exception, e:
            print "[Communicate Error]", e
    def close(self):
        """
        关闭连接
        """
        if self.handler:
            self.handler.close()
    def send(socket=None, pkg=None):
        if socket is None or pkg is None or event is None: return
        socket.sendall(pkg)
    
    def receive(socket=None):
        # 接受函数，拆包并将其通知出去
        return unpack(socket)

    def send_and_receive(self, cid=None, action=None):
        """
        # 发送并接受包
        # 返回拆开的包
        """
        print "send and receive", cid, action
        pkg = make_controller_package(cid, action)
        print pkg
        # TODO: 这里需要经一步安全的发送数据
        try:
            self.handler.sendall(pkg)
        except Exception, e:
            print "[communicate]:", e
            self.close()
            self.connect()
            self.handler.sendall(pkg)
        # 返回解析好的数据包(body, version, length)
        return unpack(self.handler)


class SyncService(object):
    """
    # 同步服务
    """
    # rooms = {
    #   [:roomId]: ([:signature], [gevent.Event()])
    # }
    rooms = {}
    json_body = {
        "uri": "device/controller/sync",
        "type": "request",   
    }
    def __init__(self, address=("10.18.50.66", "9001"), interval=4):
        """
        创建连接句柄
        """
        # 这个信道用于和中间件进行同步
        print "[Sync Service]:", address, interval
        self.address = address
        self.handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.package = pack(self.json_body)
        self.interval = interval
        # self.scheduler = sched.scheduler(time.time, time.sleep)
        self.send_timer = Timer(interval, self.__send())
        self.receive_timer = Timer(interval, self.__receive())

    def connect(self):
        try:
            self.handler.connect(self.address)
        except Exception, e:
            print "[SyncService Error]", e
        
    def update(self, room_id):
        """
        # 更新函数，用于返回request请求
        """
        print "here is update"
        # 获取唤醒时从哪里获得的
        data = room[str(room_id)][1].get()
        return data

    def __send(self):
        """
        # 发送同步请求
        """
        self.handler.sendall(self.package)

    def __receive(self):
        """
        # 接收函数，并进行拆包
        """
        # 从缓冲区读取数据
        body, version, length = unpack(self.handler)
        msg = encode_body(body)
        data = msg["data"]
        signature = sign(data)  # 数据签名
        room_id = data["roomId"]
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
        
    def start(self):
        """
        # 用于处理和服务器同步的函数
        """
        print "start.sync..."
        # 定时发送同步请求
        # self.scheduler.enter(self.interval, 1, self.__send(), ())
        # self.scheduler.enter(self.interval, 1, self.__receive(), ())
        self.send_timer.start()
        self.receive_timer.start()

    def stop(self):
        """
        # 用于暂停同步函数
        """
        print "stop sync..."
        self.send_timer.cancel()
        self.receive_timer.cancel()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import Queue
import select
import socket
import pyodbc
import threading
from time import *
from datetime import *
from threading import Event 
from signal import signal, SIGINT
from binascii import a2b_hex, b2a_hex

# 环境限定范围，由单独的线程负责不断刷新，键为房间号，值为一个队列，长度始终为2，
# 其中第一个值为包含了当前使用的环境限定范围的元组，第二个值下一次刷新时间
threshold = {}
THRESHOLD_LOAD_CYCLE = 5

arm_client_list = []
arm_client_dic = {}
django_client_list = []
django_client_dic = {}

#: 全局标志集
GLOBAL_FLAG = {
        "SYSTEM_STOP" : 1,
        }

#============任务队列模块配置==============#
#: 任务超时
TASK_TIMEOUT = 5
task_state = (0, 1, 2)

#============套接字队列模块配置=============#
#: select 超时时间
SELECT_TIMEOUT = 2
#: 僵尸套接字连接判断时间
SOCKET_TIMEOUT = 10
#: 对 ARM 提供链接服务的地址及端口
# ARM_SERVER_ADDR = ('127.0.0.1', 10001)
ARM_SERVER_ADDR = ('10.18.50.66', 9000)
#: 对 Django 提供链接服务的地址及端口 
# DJANGO_SERVER_ADDR = ('192.168.1.250', 10002)
DJANGO_SERVER_ADDR = ('10.18.50.66', 9001)

#: 方向，本系统中包括 ARM 和 Django
# from mesgtype_pb2 import *
# BIRTH_TYPE_DJANGO   = MANUAL
# BIRTH_TYPE_ARM      = AUTO
BIRTH_TYPE_MANUAL    = 0
BIRTH_TYPE_AUTO      = 1

#==============数据库模块配置=============#
#: 数据库连接参数
db_conn_info = {
    # "HOST"      : "localhost",
    "HOST": "10.18.50.66",
    "USER"      : "wsngump",
    "PASSWORD"  : "wsngump",
    "DATABASE"  : "mushroom",
    }

#=============日志模块配置===============#
#: 日志配置参数
log_conf = {
    'ERROR'           : 1,
    'COMMUMICATION'   : 1,
    'DEBUG'           : 1,
    'WORK'            : 1,
    }

log_file = {
            'ERROR' : 'E:\workspace\mushroom\log\error.txt',
            'COMMUNICATION' : 'E:\workspace\mushroom\log\communication.txt',
            'WORK'  : 'E:\workspace\mushroom\log\work.txt',
            'DEBUG' : 'E:\workspace\mushroom\log\debug.txt',
            }

# from log_manager import LogManager
#: 全局日志管理器
# log_manager = LogManager()

#=============通信协议模块配置===============#
#----- 控制端——>数据层 -------#
#: 数据包头标志
A_HEAD = 'MUSHROOM'
#: 数据包结束符
A_END = a2b_hex('13')
#: 与Django通信信息包的版本号
A_VERSION = 1
#: 数据包长度占字节数
byte_pkg_len = 3
#: 数据包版本号
byte_version = 2
#: 业务层消息头占字节数
byte_m_header_len = 3

#: 与Django通信消息包的头标志
D_HEAD = 'MUSHROOM'
#: 与Django通信信息包的版本号
D_VERSION = 1
#: 数据包版本号
D_version_byte = 1
#: 业务层消息头占字节数
D_lenght_byte = 4

#: 控制命令取值
ctrl_cmd = {
            'ON' : '1',
            'OFF': '0',
            }

# ------ 数据层 ——> 控制层 ---------#

#: 控制器设置结果
ctrl_result = {
             'SUCCESS'  : '0',
             'FAIL'     : '1',
             }
#: 控制器状态检测结果
check_state_result = {
              'ON' : '1',
              'OFF': '0',
                      }

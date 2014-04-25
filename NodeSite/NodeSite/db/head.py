#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import Queue
import ctypes
import select
import socket
import pyodbc
import logging
import threading
from time import *
from datetime import *
from threading import Event, Timer
from signal import signal, SIGINT
from binascii import a2b_hex, b2a_hex

sys_config_dict = {
              'TIME_SYNC_CYCLE' : 50,
              }

room_dict = {
             'sensor': [],
             'controller': [],
             }

# 开
ON = 1
# 关
OFF = 0
# 成功
SUC = 0
# 失败
FAI = -1
# 异常
ERR = -2

# 环境限定范围，由单独的线程负责不断刷新，键为房间号，值为一个队列，长度始终为2，
# 其中第一个值为包含了当前使用的环境限定范围的元组，第二个值下一次刷新时间
threshold = {}
#:环境限制条件载入周期
THRESHOLD_LOAD_CYCLE = 5

arm_client_list = []
arm_client_dic = {}
django_client_list = []
django_client_dic = {}


#============任务队列模块配置==============#
#: 任务超时时长（s）
TASK_TIMEOUT = 5
#:任务就绪状态
TASK_READY = 0
#:任务等待状态
TASK_WAITING = 1
#:任务完成状态
TASK_FINISHED = 2
#:最大任务号
MAX_TASK_ID = 99999
# 任务线程条件变量等待周期
TASK_WAIT_CIRCLE = 1

#============套接字队列模块配置=============#
#: select 超时时间
SELECT_TIMEOUT = 2
#: 僵尸套接字连接判断时间
SOCKET_TIMEOUT = 10
#: 对 ARM 提供链接服务的地址及端口
# ARM_SERVER_ADDR = ('127.0.0.1', 10001)
ARM_SERVER_ADDR = ('10.18.50.66', 9000)
#: 对 Django 提供链接服务的地址及端口 
# DJANGO_SERVER_ADDR = ('127.0.0.1', 10002)
DJANGO_SERVER_ADDR = ('10.18.50.66', 9001)

#: 方向，本系统中包括 ARM 和 Django
# from mesgtype_pb2 import *
# BIRTH_TYPE_DJANGO   = MANUAL
# BIRTH_TYPE_ARM      = AUTO
BIRTH_TYPE_MANUAL    = 0
BIRTH_TYPE_AUTO      = 1

#==============数据库模块配置=============#
#: 数据库连接参数
db_conn_info1 = {
    "HOST"      : "10.18.50.66",
    "USER"  : "wsngump",
    "PASSWORD"  : "wsngump",
    "DATABASE"  : "mushroom",
    }
db_conn_info2 = {
    "HOST"      : "10.18.50.10",
    "USER"      : "sa",
    "PASSWORD"  : "wsngump",
    "DATABASE"  : "mushroom",
    }
db_conn_info = db_conn_info1

#=============日志模块配置===============#
#: 日志配置参数
log_conf = {
    'ERROR'           : ON,
    'COMMUNICATION'   : ON,
    'DEBUG'           : ON,
    'WORK'            : ON,
    }

log_file = {
            'ERROR' : 'E:\workspace\mushroom\log\error.txt',
            'COMMUNICATION' : 'E:\workspace\mushroom\log\communication.txt',
            'WORK'  : 'E:\workspace\mushroom\log\work.txt',
            'DEBUG' : 'E:\workspace\mushroom\log\debug.txt',
            }

LOG_TIMER_CYCLE = 1

#=============通信协议模块配置===============#
#----- 控制端——>数据层 -------#
#: 数据包头标志
A_HEAD = 'MUSHROOM'
#: 数据包结束符
A_END = a2b_hex('13')
#: 与Django通信信息包的版本号
A_VERSION = 1
#: 数据包长度占字节数
A_pkg_byte = 3
#: 数据包版本号
# A_version_byte = 2
#: 业务层消息头占字节数
A_header_byte = 3
#收数据超时
RECV_TIMEOUT = 3    

#: 与Django通信消息包的头标志
D_HEAD = 'MUSHROOM'
#: 与Django通信信息包的版本号
D_VERSION = 1
#: 数据包版本号
D_version_byte = 1
#: 业务层消息头占字节数
D_lenght_byte = 4

POLICY_NEW = 2
POLICY_RUNNING = 1
POLICY_OLD = 0
# #: 控制命令取值
# ctrl_cmd = {
#             'ON' : '1',
#             'OFF': '0',
#             }
# 
# # ------ 数据层 ——> 控制层 ---------#
# 
# #: 控制器设置结果
# ctrl_result = {
#              'SUCCESS'  : '0',
#              'FAIL'     : '1',
#              }
# #: 控制器状态检测结果
# check_state_result = {
#               'ON' : '1',
#               'OFF': '0',
#                       }


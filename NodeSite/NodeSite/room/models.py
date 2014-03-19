# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Room(object):
    """
    房间对象，用于处理和房间相关的事务
    """
    def __init__(self):
        """
        初始化函数。
        """
        self.id = 1
        self.name = "room1"
    def set_name(self, name):
        self.name = name
    def set_plant_name(self, name):
        self.plant.name = name
    
        
class RoomManagy(object):
    def __init__(self):
        pass
        
        

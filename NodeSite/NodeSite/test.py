# -*- coding: utf-8 -*-

# Create your models here.
class Room(object):
    """
    房间对象，用于处理和房间相关的事务
    """
    __name = "room1"
    def __init__(self):
        """
        """
        self.id = 1
    def set(self, **kwargs):
        # self.name = kwargs.get("name")
        print kwargs.keys()
        
if __name__ == '__main__':
    r = Room()
    r.set(aa='hello')
    r._Room__name = 100
    print dir(r)
    print r._Room__name

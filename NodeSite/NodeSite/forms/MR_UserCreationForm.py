# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm

class MR_UserCreationForm(UserCreationForm):
    """
    Mushroom 用户创建类
    """
    
    def __init__(self, *args, **kwargs):
        """
        
        Arguments:
        - `*args`:
        - `**kwargs`:
        """
        
        return self

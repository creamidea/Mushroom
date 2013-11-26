# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core import validators

from django.db import models

from django.utils.http import urlquote
from django.utils import timezone

# Create your models here.

class User(object):
    """
    创建用户
    """
    
    def __init__(self):
        """
        """
        
        pass

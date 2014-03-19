# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core import validators

from django.contrib.auth.models import (BaseUserManager, Group)

from django.db import models

from django.utils.http import urlquote
from django.utils import timezone

# Create your models here.

class MRUser(BaseUserManager):
    """
    创建用户
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and saves a User with the given username, email and password
        """
        now = timezone.now()
        if not username:
            raise ValueError(u'必须设置用户名')
        email = BaseUserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

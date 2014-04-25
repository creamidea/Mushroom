# -*- coding: utf-8 -*-
# Create your models here.
# https://github.com/creamidea/Mushroom/issues/33

from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.utils.http import urlquote
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (User, AbstractBaseUser, AbstractUser, BaseUserManager, Group)

class MushroomUserManager(BaseUserManager):
    """
    # Mushroom房管理系统用户管理
    # 创建用户
    # 
    """
    
    def create_user(self, username, email=None, password=None, phone=None, **extra_fields):
        """
        Create and saves a User with the given username, email and password
        """
        now = timezone.now()
        if not username:
            raise ValueError(u'必须设置用户名')
        email = BaseUserManager.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, phone, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.phone = phone
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u
    
class MushroomUser(AbstractUser):
    phone = models.CharField(u"phone", max_length=11,
                             help_text=u'通知用户的紧急号码', blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    objects = MushroomUserManager()
    
    class Meta(AbstractUser.Meta):
        # app_label = 'mushroom'
        
        # 这里可以参考https://github.com/creamidea/Mushroom/issues/33
        db_table = 'auth_user'
        # verbose_name = _('user')
        # verbose_name_plural = _('users')
        # abstract = True
        swappable = 'AUTH_USER_MODEL'

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

# class MushroomUserProfile(models.Model):
#     user = models.OneToOneField(User)

# def create_mushroom_user_profile(sender, instance, create, **kwargs):
#     if create:
#         MushroomUserProfile.objects.create(user=instance)
# post_save.connect(create_mushroom_user_profile, sender=User)


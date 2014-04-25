# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from models import MushroomUser

IDENTITY = [('admin', '超级管理员'), ('user', '普通用户')]
class MushroomUserCreationFrom(UserCreationForm):
    phone = forms.RegexField(label=u"手机号码", max_length=11,
                             regex=r'^\d{11}$',
                             help_text=u'这个是用于通知用户系统紧急情况')
    # identify = forms.ChoiceField(label=u'注册身份', choices=IDENTITY, widget=forms.RadioSelect())
    # email = forms.EmailField(label=u"邮件地址", help_text=u"这个用于邮寄系统情况的地址")

    class Meta:
        model = MushroomUser
        # fields = ("username", "password1", "password2", "groups")
        fields = ("username", "password1", "password2", "phone", "email", "groups")
        # , "identify")
        # "user_permissions"
        # is_superuser",

    def save(self, commit=True):
        user = super(MushroomUserCreationFrom, self).save(commit=False)
        user.set_phone(self.cleaned_data["phone"])
        if commit:
            user.save()
        group = (self.cleaned_data["groups"]).get() # 得到组的名称
        g = Group.objects.get(name=group)           # 得到组的对象/模型
        user.groups.add(g)                          # 将用户将入该组
        return user

    # def clean_phone(self):
    #     phone = self.cleaned_data["phone"]        

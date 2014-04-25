# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from models import MushroomUser
# , MushroomUserProfile

print "Start create permission"
ct = ContentType.objects.get(app_label='account', model='mushroomuser')
vote_permission, create = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=ct)

print "Start creating account..."
admin_group, a_create = Group.objects.get_or_create(name='admin')
if a_create:
    admin_group.permissions = [vote_permission]
    admin_group.save()
user_group, u_create = Group.objects.get_or_create(name='user')
if u_create:
    user_group.save()



# content_type = ContentType.objects.get(app_label='account', model='MushroomUser')
# p, created = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)
# p = Permission.objects.get_or_create(codename=u"can_vote", name=u"can vote", content_type=content_type)

# new_user.user_permissions.add(p)
# return HttpResponseRedirect(reverse('singin'))

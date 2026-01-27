# users/signals.py
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    from django.contrib.auth.models import Group  # ✅ استيراد داخلي
    Group.objects.get_or_create(name='ServiceProviders')
    Group.objects.get_or_create(name='ServiceConsumers')

@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group  # ✅ استيراد داخلي
    if created:
        group_name = 'ServiceProviders' if instance.user_type == 'SP' else 'ServiceConsumers'
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
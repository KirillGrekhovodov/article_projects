import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from accounts.models import Profile


@receiver(pre_save, sender=Profile)
def my_handler(sender, instance, **kwargs):
    print(instance.avatar, "avatar")
    if instance.id:
        old_profile = Profile.objects.get(pk=instance.pk)
        print(old_profile.avatar, "old_file")
        if old_profile.avatar and (not instance.avatar or old_profile.avatar.path != instance.avatar.path):
            if os.path.exists(old_profile.avatar.path):
                os.remove(old_profile.avatar.path)


@receiver(post_delete, sender=Profile)
def my_handler(sender, instance, **kwargs):
    if instance.avatar and os.path.exists(instance.avatar.path):
        os.remove(instance.avatar.path)

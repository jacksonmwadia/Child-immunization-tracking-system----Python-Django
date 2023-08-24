from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Parent, Doctor, Profile,MOH

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.is_parent:
           Parent.objects.create(user=instance)
        if instance.is_ministry:
            MOH.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    if instance.is_parent:
        instance.parent.save()
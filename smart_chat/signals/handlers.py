from django.db.models.signals import post_save
from django.dispatch import receiver

from smart_chat.models import (
    Chat,
    Schedule
)


@receiver(post_save, sender=Chat)
def saved_chat(sender, instance, created, **kwargs):
    """
    database trigger after we make a successful manipulation to an object
    """
    if created:
        Schedule.objects.create(chat=instance)

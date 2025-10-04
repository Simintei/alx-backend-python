from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update (not a new message)
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        
        if old_message.content != instance.content:
            # Save old content into history
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            # Mark as edited
            instance.edited = True

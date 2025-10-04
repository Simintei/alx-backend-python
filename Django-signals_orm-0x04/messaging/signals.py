from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

#  Already implemented earlier for logging edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.edited_by  # Save who edited
            )
            instance.edited = True


#  Cleanup after user deletion
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()

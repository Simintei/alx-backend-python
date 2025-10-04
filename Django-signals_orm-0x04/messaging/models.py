from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a given user."""
    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
            .select_related("sender", "receiver")
            .only("id", "sender__username", "receiver__username", "content", "timestamp")
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    parent_message = models.ForeignKey(  # ✅ threaded replies
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)  # ✅ track if message is read

    # Managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # ✅ custom unread manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.content[:20]}"

    def get_all_replies(self):
        """
        Recursive function to fetch all nested replies in threaded format.
        """
        replies = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            replies.append({
                "message": reply,
                "replies": reply.get_all_replies()
            })
        return replies


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        related_name="message_edits",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

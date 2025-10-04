from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a given user.
    Use .only() to fetch only the necessary fields for the inbox view.
    """
    def unread_for_user(self, user):
        return (
            self.get_queryset()
                .filter(receiver=user, read=False)
                .select_related("sender", "receiver")
                .only("id", "content", "timestamp", "sender_id", "receiver_id")
        )

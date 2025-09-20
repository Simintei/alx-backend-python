import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ==========================
# 1. Custom User Model
# ==========================
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds fields not included in the default User model.
    """
    # Replace default primary key with UUID
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # These already exist in AbstractUser but included for clarity
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    # Override email to be unique + required
    email = models.EmailField(unique=True, blank=False)

    # Add phone number
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    # Password hash (Django handles hashing)
    password = models.CharField(max_length=128, blank=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ==========================
# 2. Conversation Model
# ==========================
class Conversation(models.Model):
    """
    A Conversation model that tracks which users are in the conversation.
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(
        User, related_name="conversations", blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participants = ", ".join([str(user) for user in self.participants.all()])
        return f"Conversation {self.conversation_id} between {participants}"


# ==========================
# 3. Message Model
# ==========================
class Message(models.Model):
    """
    Message model containing sender, conversation, and body.
    """
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"[:50]

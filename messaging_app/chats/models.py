import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # Added for timestamp defaults

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

    # === FIXES FOR SystemCheckError (fields.E304) ===
    # These explicit definitions with unique related_name arguments are necessary 
    # to avoid reverse accessor clashes with the built-in auth.User model,
    # resolving the SystemCheckError. 
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="chats_user_set",
        related_query_name="chats_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="chats_permission_set",
        related_query_name="chats_user",
    )
    # ===============================================

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# =========================================================================
# NEW MODELS: Conversation and Message
# =========================================================================

class Conversation(models.Model):
    """
    Represents a chat conversation between two or more users.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    
    # Many-to-Many relationship with the custom User model
    # related_name='conversations' allows retrieving all conversations for a user: user.conversations.all()
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="The users involved in this conversation"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        # Display the emails of the participants for easy identification
        return f"Conversation ({', '.join([str(p.email) for p in self.participants.all()])})"

class Message(models.Model):
    """
    Represents a single message sent within a conversation.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # Foreign Key to the Conversation this message belongs to
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )

    # Foreign Key to the User who sent the message
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )

    content = models.TextField(blank=False)
    
    # Automatically set the timestamp when the message is created
    timestamp = models.DateTimeField(default=timezone.now) 
    
    # Optional: Track if the message has been read by the recipient(s)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.email} in Conv {self.conversation.id}"

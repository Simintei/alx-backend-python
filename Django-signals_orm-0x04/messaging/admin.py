from django.contrib import admin
from .models import Message, MessageHistory, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp", "content", "edited", "parent_message")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("edited", "timestamp")

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "edited_at", "edited_by")
    search_fields = ("old_content", "edited_by__username")
    list_filter = ("edited_at",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    search_fields = ("user__username", "message__content")
    list_filter = ("is_read", "created_at")

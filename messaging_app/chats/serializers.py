from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Includes basic information but excludes password hash by default.
    """
    class Meta:
        model = User
        # We don’t expose password in API responses
        exclude = ['password', 'groups', 'user_permissions']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Shows sender info nested using UserSerializer.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'conversation'
        ]
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Shows participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_messages(self, obj):
        """
        Return serialized messages in the conversation.
        """
        messages = obj.message_set.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

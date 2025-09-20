from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Includes basic information but excludes password hash by default.
    """
    password = serializers.CharField(write_only=True)  # explicit CharField

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        """
        Override create to hash password correctly.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Shows sender info nested using UserSerializer.
    """
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # explicit CharField

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

    def validate_message_body(self, value):
        """
        Ensure message body is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


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

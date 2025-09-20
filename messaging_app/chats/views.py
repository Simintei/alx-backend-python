from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.
    GET /conversations/ -> list user conversations
    POST /conversations/ -> create a new conversation with participants
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict conversations to those the current user participates in.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Accepts a list of participant IDs.
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)  # add current user
        users = User.objects.filter(id__in=participant_ids)
        conversation.participants.add(*users)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages in a conversation.
    GET /messages/?conversation=<id> -> list messages in that conversation
    POST /messages/ -> send a message
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by conversation ID.
        """
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        """
        Attach sender and conversation when sending a message.
        """
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)


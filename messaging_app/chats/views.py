from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import generics, permissions
from.permissions import IsOwner, IsParticipantOfConversation

#conversation
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]  # <-- added
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "At least one participant required"}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        users = User.objects.filter(id__in=participant_ids)
        conversation.participants.add(*users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#messages
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]  # <-- added
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)


# Messages
class UserMessagesView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Message.objects.all()

# Conversations
class UserConversationsView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Conversation.objects.all()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # When creating a conversation, automatically add the creator as participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Only messages in conversations where the user is a participant
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        # Automatically set the sender to the logged-in user
        serializer.save(sender=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

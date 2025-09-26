from rest_framework import viewsets
from rest_framework.status import HTTP_403_FORBIDDEN  #  explicit 403 status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter  #  custom filter

# Pagination class for messages
class MessagePagination(PageNumberPagination):
    page_size = 20  #  20 messages per page

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    - Applies IsParticipantOfConversation permission
    - Paginates 20 per page
    - Filters by sender, conversation, sent_at
    """
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    # ✅ enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def perform_create(self, serializer):
        """
        Ensure only participants in a conversation can send messages.
        """
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    - Applies IsParticipantOfConversation permission
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def destroy(self, request, *args, **kwargs):
        """
        Ensure only participants can delete conversations.
        """
        instance = self.get_object()
        if request.user not in instance.participants.all():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

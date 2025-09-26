from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Base router for conversations
router = routers.DefaultRouter()  # top-level router
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages inside conversations
conversations_router = routers.NestedDefaultRouter(
    router,
    r'conversations',
    lookup='conversation'
)
conversations_router.register(
    r'messages', MessageViewSet, basename='conversation-messages'
)

urlpatterns = [
    path('messages/', UserMessagesView.as_view(), name='user-messages'),
    path('messages/<int:pk>/', UserMessageDetailView.as_view(), name='user-message-detail'),
    path('conversations/', UserConversationsView.as_view(), name='user-conversations'),
    path('conversations/<int:pk>/', UserConversationDetailView.as_view(), name='user-conversation-detail'),
]


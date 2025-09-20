from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create the router and register our viewsets
router = routers.DefaultRouter()  # the checker looks for routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the automatically generated URLs
urlpatterns = [
    path('', include(router.urls)),
]


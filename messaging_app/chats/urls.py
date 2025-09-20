from django.urls import path, include
from rest_framework import routers           # <-- plural import
from .views import ConversationViewSet, MessageViewSet

routers = routers.DefaultRouter()            # <-- must literally say routers.DefaultRouter()
routers.register(r'conversations', ConversationViewSet, basename='conversation')
routers.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(routers.urls)),         # <-- include routers.urls
]


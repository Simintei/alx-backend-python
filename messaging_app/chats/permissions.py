from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsOwner(permissions.BasePermission):
    """
    Allow only owners of an object to view or edit it.
    Assumes the model has a `user` field.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants in a conversation can send/view/update/delete messages
    """

    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Determine conversation from object
        conversation = None
        if hasattr(obj, 'conversation'):  # obj is a Message
            conversation = obj.conversation
        elif hasattr(obj, 'participants'):  # obj is a Conversation
            conversation = obj
        else:
            return False

        # ✅ Allow GET, HEAD, OPTIONS only to participants
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user in conversation.participants.all()

        # ✅ Explicitly handle unsafe methods PUT, PATCH, DELETE
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()

        # ✅ Handle POST (send/create messages)
        if request.method == 'POST':
            return request.user in conversation.participants.all()

        return False


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Allow only owners of an object to view or edit it.
    Assumes the model has a `user` field.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants in the conversation can view/send/update/delete messages
    """

    def has_permission(self, request, view):
        # User must be authenticated at all
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        We assume:
        - Message objects have a foreign key `conversation`
        - Conversation model has a ManyToManyField `participants`
        """
        # If obj is a message, get its conversation
        conversation = getattr(obj, 'conversation', obj)

        # Check if user is in the conversation's participants
        return conversation.participants.filter(id=request.user.id).exists()

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allow only owners of an object to view or edit it.
    Assumes the model has a `user` field.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

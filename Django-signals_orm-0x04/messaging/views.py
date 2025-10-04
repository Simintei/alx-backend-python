from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()  # triggers post_delete signal
    return redirect("home")


@login_required
def view_conversation(request, user_id):
    """
    View conversation between the logged-in user and another user.
    Uses select_related + prefetch_related for efficiency.
    """
    other_user = get_object_or_404(User, pk=user_id)

    messages = (
        Message.objects.filter(sender=request.user, receiver=other_user)
        | Message.objects.filter(sender=other_user, receiver=request.user)
    ).select_related("sender", "receiver") \
     .prefetch_related("replies__sender", "replies__receiver") \
     .order_by("timestamp")

    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })


@login_required
def inbox_unread(request):
    """
    Display only unread messages for the logged-in user.
    Optimized with .only() from custom manager.
    """
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, "messaging/inbox.html", {
        "unread_messages": unread_messages
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from messaging.models import Message


@login_required
@cache_page(60)   # ✅ Cache this view for 60 seconds
def view_conversation(request, user_id):
    """
    View conversation between the logged-in user and another user.
    Cached for 60 seconds to reduce repeated DB queries.
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

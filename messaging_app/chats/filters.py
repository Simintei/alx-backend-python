import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by sender username, conversation id and sent_at date range
    """
    sender = django_filters.CharFilter(
        field_name='sender__username', lookup_expr='icontains'
    )
    conversation = django_filters.NumberFilter(
        field_name='conversation__conversation_id'
    )
    start_date = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte'
    )
    end_date = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='lte'
    )

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="pass123")
        self.receiver = User.objects.create_user(username="bob", password="pass123")

    def test_message_creates_notification(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )
        notification = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertTrue(notification.exists())
        self.assertEqual(notification.count(), 1)

from django.test import TestCase
from .models import Message

class MessageModelTest(TestCase):
    def setUp(self):
        Message.objects.create(sender="admin", recipient="teacher@example.com", content="Test Content")

    def test_message_creation(self):
        message = Message.objects.get(recipient="teacher@example.com")
        self.assertEqual(message.content, "Test Content")
        self.assertEqual(message.sender, "admin")
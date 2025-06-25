from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import DocimologySession

class DocimologySessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="testpass")
        self.session = DocimologySession.objects.create(
            title="Math Exam",
            description="Desc",
            date=datetime(2023, 12, 1, 10, 0, 0),
            duration=timedelta(hours=1),
            teacher=self.user
        )

    def test_session_creation(self):
        self.assertEqual(self.session.title, "Math Exam")
        self.assertEqual(self.session.teacher, self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.session), "Math Exam")
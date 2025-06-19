from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Exam

class ExamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="testpass")
        self.exam = Exam.objects.create(subject="Mathematics", exam_date=datetime(2023, 12, 1, 10, 0, 0), duration=timedelta(hours=1), notifications="")
        self.exam.required_teachers.add(self.user)

    def test_exam_creation(self):
        exam = Exam.objects.get(subject="Mathematics")
        self.assertEqual(exam.subject, "Mathematics")
        self.assertIn(self.user, exam.required_teachers.all())
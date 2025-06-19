from django.db import models
from django.contrib.auth.models import User

class ExamCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    titre = models.CharField("Titre de l'épreuve", max_length=200, default="Titre à renseigner")
    subject = models.CharField("Salle/Amphi", max_length=100)
    promotion = models.CharField("Promotion", max_length=100, blank=True)
    exam_date = models.DateTimeField()
    duration = models.DurationField("Durée (minutes)")
    required_teachers_count = models.PositiveIntegerField(default=1, verbose_name="Required Teachers")
    notifications = models.TextField(blank=True)
    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)

    def __str__(self):
        return self.titre

    def teachers_needed(self):
        return max(0, self.required_teachers_count - self.participations.filter(is_cancelled=False).count())

    def is_full(self):
        return self.teachers_needed() <= 0

class ExamParticipation(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='participations')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.teacher.username} - {self.exam.subject}"
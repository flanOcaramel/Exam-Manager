from django.db import models
from django.contrib.auth.models import User

class DocimologySession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    is_distanciel = models.BooleanField("Distanciel", default=False)
    salle = models.CharField("Salle de la réunion", max_length=100, blank=True)
    specialite = models.CharField("Spécialité concernée", max_length=100, blank=True)
    responsable1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='docimology_responsable1', verbose_name="Responsable n°1 de la séance")
    responsable2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='docimology_responsable2', verbose_name="Responsable n°2 de la séance")
    nb_questions = models.PositiveIntegerField("Quantité de questions", default=0)
    programme = models.TextField("Programme de la séance", blank=True)
    date_examen = models.DateField("Date de l'examen", null=True, blank=True)
    required_teachers_count = models.PositiveIntegerField("Nombre de professeurs requis", default=1)
    is_responsable = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    def teachers_needed(self):
        return max(0, self.required_teachers_count - self.participations.filter(is_cancelled=False).count())

    def is_full(self):
        return self.teachers_needed() <= 0

class TeacherRole(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SessionAttendance(models.Model):
    session = models.ForeignKey(DocimologySession, on_delete=models.CASCADE, related_name='participations')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    is_responsable = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.username} - {self.session.title}"
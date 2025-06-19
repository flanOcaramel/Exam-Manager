from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_flash = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'


class FlashMessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'FlashMessage created at {self.created_at}'


class UsefulInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
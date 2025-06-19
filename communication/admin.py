from django.contrib import admin
from .models import Message

admin.site.register(Message)
# admin.site.register(Announcement)  # Décommente ou ajoute si le modèle existe

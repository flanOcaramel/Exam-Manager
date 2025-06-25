from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('view-messages/', views.list_messages, name='view_messages'),
    path('flash/', views.list_flash_messages, name='list_flash_messages'),
    path('useful-info/', views.useful_info, name='useful_info'),
]
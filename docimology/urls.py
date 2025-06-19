from django.urls import path
from . import views

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('participate/<int:session_id>/<str:role>/', views.participate_session, name='participate_session'),
    path('cancel/<int:session_id>/', views.cancel_session_participation, name='cancel_session_participation'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('create/', views.create_session, name='create_session'),
    path('update/<int:session_id>/', views.update_session, name='update_session'),
    path('delete/<int:session_id>/', views.delete_session, name='delete_session'),
]
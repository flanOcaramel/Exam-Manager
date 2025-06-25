from django.urls import path
from . import views

urlpatterns = [
    path('ecos/', views.ecos_list, name='ecos_list'),
    path('facultaires/', views.facultaires_list, name='facultaires_list'),
    path('docimologie/', views.docimologie_list, name='docimologie_list'),
    path('edn/', views.edn_list, name='edn_list'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:exam_id>/edit/', views.exam_edit, name='exam_edit'),
    path('exams/<int:exam_id>/delete/', views.exam_delete, name='exam_delete'),
    path('participate/<int:exam_id>/', views.participate_exam, name='participate_exam'),
    path('cancel/<int:exam_id>/', views.cancel_participation, name='cancel_participation'),
    path('mes-inscriptions/', views.my_registrations, name='my_registrations'),
]
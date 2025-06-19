from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exam, ExamCategory, ExamParticipation
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q, F

@login_required
def exam_calendar(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_calendar.html', {'exams': exams})

@login_required
def manage_teacher_participation(request, exam_id):
    # Logic to manage teacher participation in a specific exam
    return HttpResponse(f'Manage participation for exam ID: {exam_id}')

@login_required
def exam_list(request):
    cat_id = request.GET.get('cat')
    if cat_id:
        exams = Exam.objects.filter(category_id=cat_id)
    else:
        exams = Exam.objects.all()
    exams = exams.annotate(num_part=Count('participations', filter=Q(participations__is_cancelled=False)))
    participations = ExamParticipation.objects.filter(teacher=request.user, is_cancelled=False)
    user_exam_ids = set(p.exam_id for p in participations)
    # Sépare les examens où l'utilisateur est inscrit et les autres
    exams_user = [exam for exam in exams if exam.id in user_exam_ids]
    exams_others = [exam for exam in exams if exam.id not in user_exam_ids and exam.num_part < exam.required_teachers_count]
    # Concatène : participations d'abord, puis les autres non pleins
    exams_sorted = exams_user + exams_others
    categories = ExamCategory.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams_sorted, 'categories': categories, 'user_exam_ids': user_exam_ids})

@login_required
def exam_detail(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    return render(request, 'exams/exam_detail.html', {'exam': exam})

@login_required
def exam_create(request):
    return HttpResponse('Exam creation page')

@login_required
def exam_edit(request, exam_id):
    return HttpResponse(f'Edit exam {exam_id}')

@login_required
def exam_delete(request, exam_id):
    return HttpResponse(f'Delete exam {exam_id}')

@login_required
def participate_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    participation, created = ExamParticipation.objects.get_or_create(exam=exam, teacher=request.user)
    if not created and participation.is_cancelled:
        participation.is_cancelled = False
        participation.save()
    # TODO: notification gestionnaire
    return redirect('my_registrations')

@login_required
def cancel_participation(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    participation = ExamParticipation.objects.filter(exam=exam, teacher=request.user, is_cancelled=False).first()
    if participation:
        participation.is_cancelled = True
        participation.save()
        # TODO: notification gestionnaire
    # Redirige vers la page "Mes inscriptions" après désinscription
    return redirect('my_registrations')

@login_required
def ecos_list(request):
    exams = Exam.objects.filter(category__name__iexact="ECOS")\
        .annotate(num_part=Count('participations', filter=Q(participations__is_cancelled=False)))\
        .filter(num_part__lt=F('required_teachers_count'))\
        .order_by('exam_date')
    participations = ExamParticipation.objects.filter(teacher=request.user, is_cancelled=False)
    user_exam_ids = set(p.exam_id for p in participations)
    return render(request, 'exams/exam_list.html', {'exams': exams, 'user_exam_ids': user_exam_ids})

@login_required
def facultaires_list(request):
    exams = Exam.objects.filter(category__name__iexact="Facultaires")
    exams = [exam for exam in exams if not exam.is_full()]
    participations = ExamParticipation.objects.filter(teacher=request.user)
    user_exam_ids = set(p.exam_id for p in participations)
    return render(request, 'exams/exam_list.html', {'exams': exams, 'user_exam_ids': user_exam_ids})

@login_required
def docimologie_list(request):
    from docimology.models import DocimologySession, SessionAttendance
    sessions = DocimologySession.objects.all()
    participations = SessionAttendance.objects.filter(teacher=request.user)
    user_session_ids = set(p.session_id for p in participations)
    return render(request, 'docimology/session_list.html', {'sessions': sessions, 'user_session_ids': user_session_ids})

@login_required
def edn_list(request):
    exams = Exam.objects.filter(category__name__iexact="EDN")
    exams = [exam for exam in exams if not exam.is_full()]
    participations = ExamParticipation.objects.filter(teacher=request.user)
    user_exam_ids = set(p.exam_id for p in participations)
    return render(request, 'exams/exam_list.html', {'exams': exams, 'user_exam_ids': user_exam_ids})

@login_required
def my_registrations(request):
    participations = ExamParticipation.objects.filter(teacher=request.user, is_cancelled=False)
    exams = Exam.objects.filter(id__in=[p.exam_id for p in participations])
    exams = exams.annotate(num_part=Count('participations', filter=Q(participations__is_cancelled=False)))
    user_exam_ids = set(exams.values_list('id', flat=True))
    return render(request, 'exams/my_registrations.html', {'exams': exams, 'user_exam_ids': user_exam_ids})
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import DocimologySession, SessionAttendance
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Welcome to the Docimology app!")

@login_required
def session_list(request):
    sessions = DocimologySession.objects.all()
    participations = SessionAttendance.objects.filter(teacher=request.user, is_cancelled=False)
    user_session_ids = set(p.session_id for p in participations)
    return render(request, 'docimology/session_list.html', {
        'sessions': sessions,
        'user_session_ids': user_session_ids
    })

def session_detail(request, session_id):
    return HttpResponse(f"Details of docimology session {session_id}")

def create_session(request):
    return HttpResponse("Create a new docimology session")

def update_session(request, session_id):
    return HttpResponse(f"Update docimology session {session_id}")

def delete_session(request, session_id):
    return HttpResponse(f"Delete docimology session {session_id}")

@login_required
def participate_session(request, session_id, role):
    session = DocimologySession.objects.get(id=session_id)
    is_responsable = (role == 'responsable')
    is_reviewer = (role == 'reviewer')
    SessionAttendance.objects.get_or_create(session=session, teacher=request.user, is_responsable=is_responsable, is_reviewer=is_reviewer)
    # TODO: notification gestionnaire
    return redirect('session_list')

@login_required
def cancel_session_participation(request, session_id):
    session = DocimologySession.objects.get(id=session_id)
    attendance = SessionAttendance.objects.filter(session=session, teacher=request.user, is_cancelled=False).first()
    if attendance:
        attendance.is_cancelled = True
        attendance.save()
        # TODO: notification gestionnaire
    return redirect('session_list')
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect, render
from exams.models import ExamCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
import re
from docimology.admin import admin_csv_page, export_csv_view


def home(request):
    return HttpResponse("Bienvenue sur Exam Manager !")


def dashboard(request):
    categories = ExamCategory.objects.all()
    return render(request, 'dashboard.html', {'categories': categories})


def home_redirect(request):
    return redirect('dashboard')


class ULUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    email = forms.EmailField(label="Adresse email UL", required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+@univ-lorraine\.fr$', username):
            raise forms.ValidationError('Utilisez une adresse mail prenom.nom@univ-lorraine.fr')
        return username

    def clean(self):
        cleaned_data = super().clean()
        # Synchronise username et email
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and username and email != username:
            self.add_error('email', 'L\'adresse email doit être identique au nom d\'utilisateur.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username  # username = email
        if commit:
            user.save()
        return user


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        # force username = email
        post = request.POST.copy()
        post['username'] = post.get('email', '')
        form = ULUserCreationForm(post)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ULUserCreationForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    return redirect('dashboard')


urlpatterns = [
    path('', home_redirect, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Utiliser la vue Django standard pour /logout/ (POST uniquement)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('admin/', admin.site.urls),
    
    path('exams/', include('exams.urls')),
    path('docimology/', include('docimology.urls')),
    path('communication/', include('communication.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('admin-csv/', admin_csv_page, name='admin_csv_page'),
    path('admin-csv/download/', export_csv_view, name='admin_csv_download'),
]
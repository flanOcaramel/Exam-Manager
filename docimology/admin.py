from django.contrib import admin
from django.http import HttpResponse
import csv
import io
from .models import DocimologySession, SessionAttendance, TeacherRole
from exams.models import Exam, ExamParticipation, ExamCategory
from django.contrib.auth.models import User
from django.urls import path, reverse
from django.utils.html import format_html
import pandas as pd
from django.shortcuts import render
from django.utils.timezone import is_aware
from datetime import datetime

@admin.register(DocimologySession)
class DocimologySessionAdmin(admin.ModelAdmin):
    list_display = (
        "title", "date", "is_distanciel", "salle", "specialite", "responsable1", "responsable2", "nb_questions", "programme", "date_examen", "required_teachers_count"
    )
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'date', 'duration', 'is_distanciel', 'salle', 'specialite',
                'responsable1', 'responsable2', 'nb_questions', 'programme', 'date_examen',
                'required_teachers_count',
            )
        }),
    )
    inlines = []

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv), name='export-csv'),
        ]
        return custom_urls + urls

    def export_csv(self, request):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        def remove_tz(data):
            for row in data:
                for k, v in row.items():
                    if isinstance(v, datetime) and is_aware(v):
                        row[k] = v.replace(tzinfo=None)
            return data

        # Exams by category
        for cat_name in ["ECOS", "Facultaires", "EDN"]:
            exams = Exam.objects.filter(category__name__iexact=cat_name)
            data = list(exams.values())
            data = remove_tz(data)
            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=cat_name, index=False)
            else:
                pd.DataFrame().to_excel(writer, sheet_name=cat_name, index=False)

        # Docimologie
        docimology = DocimologySession.objects.all()
        data = list(docimology.values())
        data = remove_tz(data)
        if data:
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name="Docimologie", index=False)
        else:
            pd.DataFrame().to_excel(writer, sheet_name="Docimologie", index=False)

        # Utilisateurs
        users = User.objects.all().values()
        data = list(users)
        data = remove_tz(data)
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="Utilisateurs", index=False)

        writer.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="export_exam_manager.xlsx"'
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_csv_url'] = 'export-csv/'
        extra_context['custom_export_button'] = format_html(
            '<a class="button" style="margin:10px 0;display:inline-block;padding:8px 16px;background:#28a745;color:#fff;border-radius:4px;text-decoration:none;" href="{}">⬇️ Exporter Excel (5 onglets)</a>',
            'export-csv/'
        )
        return super().changelist_view(request, extra_context=extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        context['custom_export_button'] = format_html(
            '<a class="button" style="margin:10px 0;display:inline-block;padding:8px 16px;background:#28a745;color:#fff;border-radius:4px;text-decoration:none;" href="{}">⬇️ Exporter Excel (5 onglets)</a>',
            '../export-csv/'
        )
        return super().render_change_form(request, context, *args, **kwargs)

# Ajout d'un bouton dans le header admin principal
from django.contrib import admin
from django.utils.html import format_html
from django.template.response import TemplateResponse

original_index = admin.site.index

def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    export_url = reverse('admin_csv_page')
    extra_context['custom_export_button'] = format_html(
        '<a class="button" style="position:absolute;top:20px;right:40px;padding:10px 24px;background:#28a745;color:#fff;border-radius:6px;text-decoration:none;font-size:1.1em;z-index:1000;" href="{}">⬇️ Export Excel</a>',
        export_url
    )
    response = original_index(request, extra_context=extra_context)
    return response

admin.site.index = custom_admin_index

def export_csv_view(request):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    def remove_tz(data):
        for row in data:
            for k, v in row.items():
                if isinstance(v, datetime) and is_aware(v):
                    row[k] = v.replace(tzinfo=None)
        return data

    # Exams by category
    for cat_name in ["ECOS", "Facultaires", "EDN"]:
        exams = Exam.objects.filter(category__name__iexact=cat_name)
        data = list(exams.values())
        data = remove_tz(data)
        if data:
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=cat_name, index=False)
        else:
            pd.DataFrame().to_excel(writer, sheet_name=cat_name, index=False)

    # Docimologie
    docimology = DocimologySession.objects.all()
    data = list(docimology.values())
    data = remove_tz(data)
    if data:
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="Docimologie", index=False)
    else:
        pd.DataFrame().to_excel(writer, sheet_name="Docimologie", index=False)

    # Utilisateurs
    users = User.objects.all().values()
    data = list(users)
    data = remove_tz(data)
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name="Utilisateurs", index=False)

    writer.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export_exam_manager.xlsx"'
    return response

def admin_csv_page(request):
    return render(request, 'admin/csv_export.html')
from django.contrib import admin
from .models import Exam, ExamCategory

class ExamAdmin(admin.ModelAdmin):
    list_display = ("titre", "promotion", "subject", "exam_date", "category", "required_teachers_count")
    exclude = ("is_ecos", "is_closed", "required_teachers")
    
    def required_teachers_count(self, obj):
        return obj.required_teachers_count
    required_teachers_count.short_description = "Required Teachers"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].choices = [
            (c.id, c.name) for c in ExamCategory.objects.filter(name__in=["ECOS", "Facultaires", "EDN"])
        ]
        form.base_fields["category"].label_from_instance = lambda obj: obj.name
        form.base_fields["required_teachers_count"].label = "Required Teachers"
        return form

class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(name__in=["ECOS", "Facultaires", "EDN"])
admin.site.register(ExamCategory, ExamCategoryAdmin)

admin.site.register(Exam, ExamAdmin)
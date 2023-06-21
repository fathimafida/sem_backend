import csv
from django.contrib import admin
from django import forms
from .models import Student
from api.authentication.models import CustomUser
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from api.classroom.models import ClassRoom
from api.department.models import Department


class StudentResource(resources.ModelResource):
    classroom = fields.Field(
        column_name='classroom',
        attribute='classroom',
        widget=ForeignKeyWidget(ClassRoom, 'id')
    )
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'id')
    )

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'year_of_join', 'admission_no', 'classroom', 'department', 'gender')
        export_order = fields
        import_id_fields = ('admission_no',)


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def validate_unique(self):
        super().validate_unique()
        email = self.cleaned_data.get("email")
        user_qs = CustomUser.objects.filter(email=email)
        if self.instance.pk:
            user_qs = user_qs.exclude(pk=self.instance.user.pk)
        if user_qs.exists():
            self.add_error("email", "Email must be unique for students.")


class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = StudentAdminForm
    resource_class = StudentResource


admin.site.register(Student, StudentAdmin)

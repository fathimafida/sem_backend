from django.contrib import admin
from django import forms
from api.authentication.models import CustomUser
from api.student.models import Student


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


class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm


admin.site.register(Student, StudentAdmin)

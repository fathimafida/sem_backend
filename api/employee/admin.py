from django.contrib import admin
from django import forms
from api.authentication.models import CustomUser
from api.employee.models import Employee


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_unique(self):
        super().validate_unique()
        email = self.cleaned_data.get("email")
        user_qs = CustomUser.objects.filter(email=email)
        if self.instance.pk:
            user_qs = user_qs.exclude(pk=self.instance.user.pk)
        if user_qs.exists():
            self.add_error("email", "Email must be unique for employees.")


class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm


admin.site.register(Employee, EmployeeAdmin)

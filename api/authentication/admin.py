from django import forms
from django.contrib import admin


from django.contrib.auth.admin import UserAdmin

from api.authentication.models import CustomUser

admin.site.site_title = "Sembook Admin"
admin.site.site_header = "Sembook Admin"
# Register your models here.


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate_unique(self):
        exclude = self.instance.pk
        queryset = self._meta.model.objects.filter(email=self.cleaned_data["email"])
        if queryset.exclude(pk=exclude).exists():
            self._update_errors({"email": ["Email must be unique."]})

    def clean(self):
        self.validate_unique()
        return super().clean()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff"]
    list_filter = ["is_active", "is_staff"]
    readonly_fields = ["date_joined", "last_login"]

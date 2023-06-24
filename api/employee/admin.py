from io import BytesIO
import os
import uuid
from django.contrib import admin
from django import forms
from api.authentication.models import CustomUser
from api.employee.models import Employee
from jsignature.utils import draw_signature
from django.core.files import File


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

    

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    
    list_display = ('first_name', 'last_name','id', 'email', 'role')
    
    def get_queryset(self, request):
        # Display only employee objects related to the logged-in user
        if request.user.is_superuser:
            return super().get_queryset(request)
        if hasattr(request.user, 'employee'):
            if request.user.employee.role == Employee.Roles.TEACHER:
                return Employee.objects.filter(classroom=request.user.employee.classroom)
            else:
                return super().get_queryset(request)
        # if hasattr(request.user, 'student'):
        #     return Employee.objects.filter(user=request.user)
    
    def get_exclude(self, request, obj=None):
        # Hide the 'sign' and 'user' fields in the add/change form
        
        return ['sign', 'user']
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        if hasattr(request.user, 'employee'):
            if request.user.employee.role == Employee.Roles.PRINCIPAL:    
                return super().get_readonly_fields(request, obj)
           
        
        return ['role', 'department','is_profile_completed']

    def save_model(self, request, obj, form, change):
        # Save the signature as an image
        signature = form.cleaned_data.get('signature')
        if signature:
            # Save the signature as an image
            signature_picture = draw_signature(signature)
            
            # Generate a unique name for the image file
            image_name = f'{uuid.uuid4()}.png'
         
            
            # Convert the image to bytes
            signature_bytes = BytesIO()
            signature_picture.save(signature_bytes, format='PNG')
            
            # Save the image to the sign field of the Employee model
            obj.sign.save(image_name, File(signature_bytes), save=False)
        
        # Save the model
        super().save_model(request, obj, form, change)



admin.site.register(Employee, EmployeeAdmin)

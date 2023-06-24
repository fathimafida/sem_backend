import csv
from io import BytesIO
import uuid
from django.contrib import admin
from django import forms

from api.employee.models import Employee
from .models import Student
from api.authentication.models import CustomUser
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from api.classroom.models import ClassRoom
from api.department.models import Department
from jsignature.utils import draw_signature
from django.core.files import File


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
    list_display = ['__str__', 'email', 'admission_no','classroom']
    list_filter = ('is_active','is_profile_completed')
    search_fields = ('first_name', 'last_name', 'email', 'admission_no')
    
    def get_queryset(self, request):
        # Filter the student queryset based on the logged-in user's classroom
        if request.user.is_superuser:
            return super().get_queryset(request)
        if hasattr(request.user, 'employee'):
            if request.user.employee.role == Employee.Roles.TEACHER:
                return Student.objects.filter(classroom=request.user.employee.classroom)
            else:
                return super().get_queryset(request)
        if hasattr(request.user, 'student'):
            return Student.objects.filter(user=request.user)
    
    def get_exclude(self, request, obj=None):
        # Hide the 'sign' and 'user' fields in the add/change form
        return ['user','is_profile_completed','sign','parent_sign']
        

    
    def save_model(self, request, obj, form, change):
        # Assign the logged-in user to the student object
        if not obj.classroom:
            classroom = request.user.employee.classroom
            obj.classroom = classroom
            
        if not obj.department:
            department = request.user.employee.department
            obj.department = department
            
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
        
        parent_signature = form.cleaned_data.get('parent_signature')
        
        if parent_signature:
            # Save the signature as an image
            parent_signature_picture = draw_signature(parent_signature)
            
            # Generate a unique name for the image file
            image_name = f'{uuid.uuid4()}.png'
         
            
            # Convert the image to bytes
            parent_signature_bytes = BytesIO()
            parent_signature_picture.save(parent_signature_bytes, format='PNG')
            
            # Save the image to the sign field of the Employee model
            obj.parent_sign.save(image_name, File(parent_signature_bytes), save=False)
        
        super().save_model(request, obj, form, change)


admin.site.register(Student, StudentAdmin)

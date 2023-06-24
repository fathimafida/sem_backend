from django.contrib import admin

from api.department.models import Department

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','id',)
    

admin.site.register(Department,DepartmentAdmin)

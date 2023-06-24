from django.contrib import admin

from api.classroom.models import ClassRoom

# Register your models here.


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('current_semester','name','id')

admin.site.register(ClassRoom,ClassRoomAdmin)

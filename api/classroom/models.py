from django.db import models

from api.employee.models import Employee
from api.department.models import Department


class ClassRoom(models.Model):
    class Semester(models.TextChoices):
        S1 = "S1"
        S2 = "S2"
        S3 = "S3"
        S4 = "S4"
        S5 = "S5"
        S6 = "S6"
        S7 = "S7"
        S8 = "S8"

    name = models.CharField(max_length=100)
    current_semester = models.CharField(
        choices=Semester.choices, default=Semester.S1, max_length=10
    )
    faculty = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.current_semester + " " + self.name

from django.db import models
from api.employee.models import Employee

from api.student.models import Student


class Sembook(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    principal = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={"role": Employee.Roles.PRINCIPAL},
    )
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.student.classroom.current_semester+" "+self.student.classroom.name + " " + self.student.first_name + " Sembook"

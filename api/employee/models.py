from django.db import models
from django.forms import ValidationError

from api.authentication.models import CustomUser
from api.department.models import Department
from jsignature.fields import JSignatureField



class Employee(models.Model):
    class Roles(models.TextChoices):
        TEACHER = "ADMIN"
        STAFF = "STAFF"
        PRINCIPAL = "PRINCIPAL"
        ADMIN_STAFF = "ADMIN_STAFF"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    staff_id = models.CharField(
        max_length=50,
    )
    signature = JSignatureField(null=True,blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STAFF)
    sign = models.ImageField(upload_to="sign", null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_profile_completed = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        admin_staff_count = Employee.objects.filter(role=self.Roles.ADMIN_STAFF).count()
        principal_count = Employee.objects.filter(role=self.Roles.PRINCIPAL).exclude(pk=self.pk).count()

        if self.role == self.Roles.ADMIN_STAFF and admin_staff_count > 0:
            raise ValidationError("There can only be one ADMIN_STAFF role.")
        elif self.role == self.Roles.PRINCIPAL and principal_count > 0:
            raise ValidationError("There can only be one PRINCIPAL role.")

    def __str__(self):
        return self.first_name

from django.db import models
from api.authentication.models import CustomUser
from api.classroom.models import ClassRoom

from api.department.models import Department


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True)
    year_of_join = models.IntegerField()
    admission_no = models.CharField(max_length=50)
    university_reg_no = models.CharField(null=True, blank=True, max_length=50)
    mobile = models.CharField(null=True, blank=True, max_length=50)
    sign = models.ImageField(upload_to="sign", null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True, blank=True)
    department =   models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    adhaar_no = models.CharField(null=True, blank=True, max_length=50)
    address = models.TextField(null=True, blank=True, default=None)
    blood_group = models.CharField(null=True, blank=True, max_length=50)
    hobby = models.TextField(null=True, blank=True, default=None)
    field_of_interest = models.TextField(null=True, blank=True, default=None)
    father_name = models.CharField(null=True, blank=True, max_length=150)
    mother_name = models.CharField(null=True, blank=True, max_length=150)
    father_mobile = models.CharField(null=True, blank=True, max_length=50)
    mother_mobile = models.CharField(null=True, blank=True, max_length=50)
    guardian_name = models.CharField(null=True, blank=True, max_length=150)
    guardian_relation = models.CharField(null=True, blank=True, max_length=150)
    guardian_mobile = models.CharField(null=True, blank=True, max_length=50)
    parent_email = models.EmailField(null=True, blank=True)
    parent_address = models.TextField(null=True, blank=True, default=None)
    parent_sign = models.ImageField(upload_to="sign", null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=Gender.choices, default=Gender.MALE
    )
    is_active = models.BooleanField(default=True)
    is_profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

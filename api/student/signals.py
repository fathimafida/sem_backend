from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from api.authentication.models import CustomUser
from api.employee.models import Employee
from api.sembook.models import Sembook

from api.student.models import Student
from django.contrib.auth.models import Group


@receiver(pre_save, sender=Student)
def create_user_for_student(sender, instance: Student, **kwargs):
    User = CustomUser

    # Check if the instance is being created (not updated)
    if not instance.pk:
        # Create a new User instance
        user = User.objects.create_user(
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.admission_no,
            is_staff=True
        )
        # Assign the created User to the Student's user field
        instance.user = user
        group, created = Group.objects.get_or_create(name="STG")
        
        instance.user.groups.add(group)


@receiver(pre_save, sender=Student)
def update_student_profile_completed(sender, instance: Student, **kwargs):
    if all(
        [
            instance.first_name,
            instance.last_name,
            instance.email,
            instance.user,
            instance.year_of_join,
            instance.admission_no,
            instance.university_reg_no,
            instance.mobile,
            instance.sign,
            instance.image,
            instance.classroom,
            instance.department,
            instance.adhaar_no,
            instance.address,
            instance.blood_group,
            instance.hobby,
            instance.field_of_interest,
            instance.father_name,
            instance.mother_name,
            instance.father_mobile,
            instance.mother_mobile,
            instance.guardian_name,
            instance.guardian_relation,
            instance.guardian_mobile,
            instance.parent_email,
            instance.parent_address,
            instance.parent_sign
        ]
    ):
        instance.is_profile_completed = True
        Sembook.objects.filter(student=instance).update(is_completed=True)
    else:
        instance.is_profile_completed = False


@receiver(post_delete, sender=Student)
def delete_user_with_student(sender, instance: Student, **kwargs):
    if instance.user:
        instance.user.delete()


@receiver(post_save, sender=Student)
def create_sembook(sender, instance, created, **kwargs):
    if created:
        # Retrieve the principal with the role "principal"
        principal = Employee.objects.filter(role=Employee.Roles.PRINCIPAL).first()
        
        # Create a Sembook instance for the student with the principal's signature
        Sembook.objects.create(student=instance, principal=principal,is_completed = instance.is_profile_completed)
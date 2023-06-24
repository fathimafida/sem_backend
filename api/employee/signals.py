from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from api.authentication.models import CustomUser
from django.contrib.auth.models import Group


from api.employee.models import Employee


@receiver(pre_save, sender=Employee)
def create_user_for_employee(sender, instance: Employee, **kwargs):
    User = CustomUser

    # Check if the instance is being created (not updated)
    if not instance.pk:
        # Create a new User instance
        user = User.objects.create_user(
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.staff_id,
            is_staff=True,  
        )
        # Assign the created User to the Student's user field
        instance.user = user
        if instance.role == Employee.Roles.PRINCIPAL:
            group, created = Group.objects.get_or_create(name="PG")
        if instance.role == Employee.Roles.TEACHER:
            group, created = Group.objects.get_or_create(name="TG")
        if instance.role == Employee.Roles.STAFF:
            group, created = Group.objects.get_or_create(name="SG")
        
        instance.user.groups.add(group)


@receiver(pre_save, sender=Employee)
def update_employee_profile_completed(sender, instance: Employee, **kwargs):
    if all(
        [
            instance.first_name,
            instance.last_name,
            instance.email,
            instance.user,
            instance.mobile,
            instance.role,
            instance.department,
            instance.sign,
        ]
    ):
        instance.is_profile_completed = True
    else:
        instance.is_profile_completed = False


@receiver(post_delete, sender=Employee)
def delete_user_with_employee(sender, instance: Employee, **kwargs):
    if instance.user:
        instance.user.delete()

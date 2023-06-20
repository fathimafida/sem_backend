# Generated by Django 4.2.2 on 2023-06-20 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('staff_id', models.CharField(max_length=50)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('role', models.CharField(choices=[('ADMIN', 'Teacher'), ('STAFF', 'Staff'), ('PRINCIPAL', 'Principal'), ('ADMIN_STAFF', 'Admin Staff')], default='STAFF', max_length=20)),
                ('sign', models.ImageField(blank=True, null=True, upload_to='sign')),
                ('is_active', models.BooleanField(default=True)),
                ('is_profile_completed', models.BooleanField(default=False)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
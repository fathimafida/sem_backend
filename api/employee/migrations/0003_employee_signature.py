# Generated by Django 4.2.2 on 2023-06-22 04:33

from django.db import migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_alter_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='signature',
            field=jsignature.fields.JSignatureField(null=True),
        ),
    ]
# Generated by Django 4.2.2 on 2023-06-22 07:41

from django.db import migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_signature',
            field=jsignature.fields.JSignatureField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='signature',
            field=jsignature.fields.JSignatureField(null=True),
        ),
    ]

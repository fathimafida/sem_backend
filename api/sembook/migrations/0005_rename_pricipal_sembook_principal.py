# Generated by Django 4.2.2 on 2023-06-22 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sembook', '0004_remove_sembook_principal_sign_sembook_pricipal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sembook',
            old_name='pricipal',
            new_name='principal',
        ),
    ]

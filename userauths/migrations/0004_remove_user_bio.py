# Generated by Django 4.2.1 on 2023-06-12 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_alter_user_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
    ]
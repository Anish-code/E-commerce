# Generated by Django 4.2.1 on 2023-06-12 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_remove_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

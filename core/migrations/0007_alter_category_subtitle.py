# Generated by Django 4.2.1 on 2023-06-18 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_category_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subtitle',
            field=models.CharField(default='General Medicine', max_length=100, null=True),
        ),
    ]

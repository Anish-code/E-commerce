# Generated by Django 4.2.1 on 2023-06-25 06:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_product_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='I am an amazing vendor', null=True),
        ),
    ]

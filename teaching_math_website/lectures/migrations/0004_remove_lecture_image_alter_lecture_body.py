# Generated by Django 5.1.2 on 2024-11-26 19:10

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0003_lecture_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='image',
        ),
        migrations.AlterField(
            model_name='lecture',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]

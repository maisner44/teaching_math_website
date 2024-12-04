# Generated by Django 5.1.2 on 2024-11-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0004_remove_lecture_image_alter_lecture_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='body',
            field=models.TextField(),
        ),
    ]
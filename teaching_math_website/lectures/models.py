from django.db import models

# Create your models here.
class Lecture(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Поле для загрузки изображения

    def __str__(self):
        return self.title
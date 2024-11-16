from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TEST_TYPE = [
        ('text', 'Text Answer'),
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
    ]

    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(choices=TEST_TYPE, max_length=10)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

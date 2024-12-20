from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


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
    correct_answer = models.ForeignKey(
        'Answer', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='correct_for_questions'
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    # def clean(self):
    #     # Перевірка, чи поле is_correct не None
    #     if self.is_correct is None:
    #         raise ValidationError({'is_correct': 'Поле "is_correct" є обов\'язковим для заповнення.'})
        
    #     # Перевірка, чи питання вже збережене
    #     if self.question.pk is not None:
    #         # Додатково: перевірка, щоб хоча б одна відповідь була правильною
    #         if self.question.answers.filter(is_correct=True).count() == 0 and not self.is_correct:
    #             raise ValidationError(_('Повинен бути хоча б один правильний варіант відповіді.'))
            
            
    def add_warning(self, message):
        # Додає попередження у форму, яке не блокує збереження
        if hasattr(self, 'warning_messages'):
            self.warning_messages.append(message)
        else:
            self.warning_messages = [message]
   

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.CharField(max_length=40)  # Store the raw score
    total_questions = models.IntegerField(default=0)
    result_percentage = models.CharField(max_length=10,default='')

    def __str__(self):
        return f"Result of {self.test.name} by {self.user.username}, score{self.score}"



class AnswerSelection(models.Model):
    test_result = models.ForeignKey(TestResult, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.text}: {self.answer.text}"

    @property
    def is_correct(self):
        return self.answer.is_correct
    
# Signals
@receiver(pre_save, sender=Answer)
def ensure_single_correct_answer(sender, instance, **kwargs):
    """
    If 'is_correct' is set to True, ensure no other answer for the same question has 'is_correct' set to True.
    """
    if instance.is_correct:
        Answer.objects.filter(question=instance.question, is_correct=True).update(is_correct=False)


@receiver(post_save, sender=Answer)
def update_correct_answer(sender, instance, **kwargs):
    """
    Automatically update the 'correct_answer' field of the related question if 'is_correct' is True.
    """
    if instance.is_correct:
        question = instance.question
        question.correct_answer = instance
        question.save()

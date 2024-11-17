from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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
    #     """
    #     Custom validation to prevent multiple correct answers for single-choice questions.
    #     """
    #     if self.is_correct and self.question.question_type == 'single':
    #         # Check if another answer for the same question is already marked as correct
    #         print(self.text,'-----------')
    #         print(Answer.objects.filter(question=self.question, is_correct=True).exclude(pk=self.pk),'-------------------')
    #         if Answer.objects.filter(question=self.question, is_correct=True).exclude(pk=self.pk).exists():
    #             raise ValidationError("Only one correct answer is allowed for single-choice questions.")

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)


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

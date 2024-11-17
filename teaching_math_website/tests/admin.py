from django import forms
from django.contrib import admin
from .models import Test, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

    def save_new(self, form, commit=True):
        """
        Save new inline form instances immediately.
        """
        instance = form.save(commit=commit)
        return instance


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Показуємо відповіді лише для цього питання
            self.fields['correct_answer'].queryset = Answer.objects.filter(question=self.instance)
        else:
            self.fields['correct_answer'].queryset = Answer.objects.none()


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    inlines = [AnswerInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

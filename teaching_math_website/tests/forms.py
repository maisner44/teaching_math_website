from django import forms
from .models import Question, Answer

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            if question.question_type == 'text':
                self.fields[f'question_{question.id}'] = forms.CharField(label=question.text, required=True)
            elif question.question_type == 'single':
                choices = [(answer.id, answer.text) for answer in question.answers.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(label=question.text, choices=choices, widget=forms.RadioSelect, required=True)
            elif question.question_type == 'multiple':
                choices = [(answer.id, answer.text) for answer in question.answers.all()]
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(label=question.text, choices=choices, widget=forms.CheckboxSelectMultiple, required=True)

    def get_answers(self):
        return {field.name: field.value() for field in self}

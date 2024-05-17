from django import forms
from .models import Question

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            if question.typeOfQ == 0:  # Multiple Choice
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.title,
                    choices=[(answer.id, answer.answer_text) for answer in question.answer.all()],
                    widget=forms.RadioSelect
                )
            elif question.typeOfQ == 1:  # True/False
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.title,
                    choices=[(answer.id, answer.answer_text) for answer in question.answer.all()],
                    widget=forms.RadioSelect
                )
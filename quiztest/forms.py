from django import forms

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(QuizForm, self).__init__(*args, **kwargs)

        self.fields[f'question_{question.id}'] = forms.ChoiceField(
            label=question.title,
            choices=[(answer.id, answer.answer_text) for answer in question.answer.all()],
            widget=forms.RadioSelect
        )

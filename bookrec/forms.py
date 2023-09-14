from django import forms
from bookrec.models import Submission, Choice


class SurveyForm(forms.Form):
    question_1 = forms.ChoiceField(label="question text", widget=forms.RadioSelect, choices=())

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        del self.fields["question_1"]
        for question in survey.question_set.all():
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(label=question.text, widget=forms.RadioSelect, choices=choices)

    def save(self):
        data = self.cleaned_data
        submission = Submission(survey=self.survey)
        submission.save()
        for question in self.survey.question_set.all():
            choice = Choice.objects.get(pk=data[f"question_{question.id}"])
            submission.answer.add(choice)

        submission.save()
        return submission

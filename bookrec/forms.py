from django import forms
from .models import SurveyResponse, Choice
import crispy_bootstrap4


class CombinedForm(forms.Form):
    """SurveyForm handling user input"""

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey

        self.fields['age_group'] = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput())
        self.fields['gender'] = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput())
        self.fields['book_frequency'] = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput())
        self.fields['reading_platform'] = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput())
        self.fields['genre'] = forms.CharField(max_length=8192, required=True, widget=forms.HiddenInput())
        self.fields['sessionId'] = forms.CharField(max_length=128, widget=forms.HiddenInput())

        for question in survey.question_set.all():
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            # Here the fields are dynamically created
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                choices=choices,
                required=True)

    def save(self):
        # Saving everything to a SurveyResponse Model
        survey_response = SurveyResponse(survey=self.survey)
        survey_response.sessionId = self.cleaned_data['sessionId']
        survey_response.rotation_state = self.survey.rotation_state
        survey_response.age_group = self.cleaned_data['age_group']
        survey_response.book_frequency = self.cleaned_data['book_frequency']
        survey_response.sessionId = self.cleaned_data['sessionId']
        survey_response.save()
        for question in self.survey.question_set.all():
            choice_id = self.cleaned_data[f"question_{question.id}"]
            choice = Choice.objects.get(pk=choice_id)
            survey_response.answer.add(choice)
        for gender_choice in self.cleaned_data['gender']:
            survey_response.gender += gender_choice
        for platform_choice in self.cleaned_data['reading_platform']:
            survey_response.reading_platform += platform_choice
        for genre_choice in self.cleaned_data['genre']:
            survey_response.genre += genre_choice

        survey_response.save()
        return survey_response


class DemographicForm(forms.Form):
    age_group = forms.ChoiceField(
        choices=SurveyResponse.AGE_GROUP_CHOICES,
        label='Age',
        widget=forms.Select(attrs={'class': 'custom-choice-field'}),
        required=True,
    )
    gender = forms.MultipleChoiceField(
        choices=SurveyResponse.GENDER_CHOICES,
        label='Gender (choose as many as you like)',
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    reading_platform = forms.MultipleChoiceField(
        choices=SurveyResponse.READING_PLATFORM_CHOICES,
        label='Your preferred book format (choose as many as you like)',
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    book_frequency = forms.ChoiceField(
        choices=SurveyResponse.BOOK_FREQUENCY_CHOICES,
        label='How many books are you consuming per year?',
        widget=forms.Select(attrs={'class': 'custom-choice-field'}),
        required=True,
    )
    genre = forms.MultipleChoiceField(
        choices=SurveyResponse.GENRE_CHOICES,
        label='What are your favourite book genres?',
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

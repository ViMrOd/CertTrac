from django import forms
from .models import Tutor, Takes, Session, Subtopic


class AddSessionForm(forms.Form):
    subtopic = forms.ModelChoiceField(
        queryset = Subtopic.objects.all(), 
        to_field_name = 'name', 
        label = 'Subtopic'
    )
    semester = forms.CharField(widget=forms.TextInput())
    In_Person_Hours = forms.DecimalField(max_digits = 5, decimal_places = 2)
    async_hours = forms.DecimalField(max_digits = 5, decimal_places = 2)


class AddTutorForm(forms.Form):
    first_name = forms.CharField(max_length = 40)
    last_name = forms.CharField(max_length = 40)
    email = forms.EmailField()
    date_hired = forms.CharField(max_length = 40)


class AddLoggedHours(forms.Form):
    name = forms.CharField(max_length = 80)
    date = forms.DateField()
    

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_hired',
            'level',
            'logged_25_hours_level_1',
            'level_1_completion_date',
            'logged_25_hours_level_2',
            'review_level_1_completed',
            'level_2_completion_date',
        ]


class TutorLevelForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [
            #'first_name',
            #'last_name',
            'level',
            'level_1_completion_date',
            'level_2_completion_date',
        ]


class TakesForm(forms.ModelForm):
    class Meta:
        model = Takes
        fields = []


class SessionForm(forms.ModelForm):
    subtopic = forms.ModelChoiceField(
        queryset = Subtopic.objects.all(), 
        to_field_name = 'name', 
        label = 'Subtopic'
    )
    semester = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Session
        fields = ['subtopic', 'semester', 'in_person_hours', 'async_hours']

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            initial_subtopic_name = kwargs['instance'].subtopic.name
            self.initial['subtopic'] = initial_subtopic_name


class SearchTutors(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset = Tutor.objects.all(), 
        to_field_name = 'first_name'
    )
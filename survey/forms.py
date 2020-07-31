from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator

alphaValidator = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha characters are allowed.')

from .models import Observation_Individual, Observation, Survey_Individual,Survey_IndividualExtra, Survey

# define a function to check if a string has any numbers
def hasNumbers(inString):
    return any(char.isdigit() for char in inString)

# Observation
class Observation_Individual_Form(forms.ModelForm):
    class Meta:
        model = Observation_Individual
        fields = ('client_location', 'client_homeless', 'client_age',
                  'client_gender', 'client_race', 'client_ethnicity',
                  'client_information','c_obs_user',
                )


class Observation_Form(forms.ModelForm):
    class Meta:
        model = Observation
        # Exclude from required fields for form; this allows the user to be added on the server side in views.py
        exclude = ('obs_user', 'obs_adults', 'obs_children', 'obs_unsure')

        # NOTE:
        # 1) The obs_user should be handled on our end (within views)
        # 2) The obs_householdnum is not user editable (as specified in models)
        fields = ('obs_reason', 'obs_adults', 'obs_children', 'obs_unsure',
                   'obs_client','obs_time',)

    def __init__(self, obs_user, *args, **kwargs):
        super(Observation_Form, self).__init__(*args, **kwargs)
        # Filter the obs_client objects (the individuals getting surveyed) to only query the current logged in user
        self.fields['obs_client'].queryset = Observation_Individual.objects.filter(c_obs_user=obs_user)

# Survey
# Individual
class Survey_Individual_Form(forms.ModelForm):

    class Meta:
        model = Survey_Individual
        exclude = ('client_survey_over18', 's_obs_user', 'client_survey_age_grouped') # fields to be filled in on the backend ofform
        """
        fields = ('client_survey_initials', 'client_survey_relationship', 'client_survey_hhconfirm', 'client_survey_nonhhlastnight',
                  'client_survey_age_exact', , 'client_survey_ethnicity', 'client_survey_race',
                  'client_survey_race_other', 'client_survey_gender', 'client_survey_served', 'client_survey_served_guard_res',
                  'client_survey_served_VHA', 'client_survey_benefits', 'client_surey_firsttime' , 'client_survey_homelesslength',
                  'client_survey_homelesslength_number', 'client_survey_timeshomeless', 'client_survey_timeshomeless_length',
                  'client_survey_timeshomeless_number', 'client_survey_over18')
        """
        #client_survey_initials = forms.CharField( validators=[alphaValidator])

        # this function will be used for the validation

    # Doesn't work yet
    """
    def clean(self):
        # data from the form is fetched using super function
        super(Survey_Individual_Form, self).clean()

        # extract the client inititals from data
        initials = self.cleaned_data.get('client_survey_initials')

        # condition check if the initals contain a #
        if hasNumbers(initials):
            self._errors['client_survey_initials'] = self.error_class([
                'Only alpha characters allowed for initials.'])

            # return any errors if found
        return self.cleaned_data
    """

    def __init__(self, *args, **kwargs):
        super(Survey_Individual_Form, self).__init__(*args, **kwargs)
        self.fields['client_survey_race_other'].required = False
        self.fields['client_survey_served_guard_res'].required = False
        self.fields['client_survey_served_VHA'].required = False
        self.fields['client_survey_benefits'].required = False

        # Individual Extra
class Survey_Individual_Extra_Form(forms.ModelForm):
    class Meta:
        model = Survey_IndividualExtra
        fields = ('client_survey_substance', 'client_survey_mhealth', 'client_survey_phealth', 'client_survey_stablehousing',
                  'client_survey_barriers', 'client_survey_specialed', 'client_survey_HIVAIDS', 'client_survey_DV')

    def __init__(self, *args, **kwargs):
        super(Survey_Individual_Extra_Form, self).__init__(*args, **kwargs)
        self.fields['client_survey_substance'].required = False
        self.fields['client_survey_mhealth'].required = False
        self.fields['client_survey_phealth'].required = False
        self.fields['client_survey_stablehousing'].required = False
        self.fields['client_survey_barriers'].required = False
        self.fields['client_survey_specialed'].required = False
        self.fields['client_survey_HIVAIDS'].required = False
        self.fields['client_survey_DV'].required = False

# Survey General
class Survey_Form(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ('survey_user', 'survey_adults', 'survey_children',) # fields to be filled in on the backend of form
        fields = ('survey_lastnight', 'survey_repeat', 'survey_client', 'survey_user')

    def __init__(self, survey_user, *args, **kwargs):
        super(Survey_Form, self).__init__(*args, **kwargs)
        # Filter the Survey_Individual objects (the individuals getting surveyed) to only query the current logged in user
        self.fields['survey_client'].queryset = Survey_Individual.objects.filter(s_obs_user=survey_user)


# User Creation Forms
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Please enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Please enter your last name.')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
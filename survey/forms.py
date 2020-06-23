from django import forms

from .models import Observation_Individual, Observation, Survey_Individual, Survey

# Observation
class Observation_Individual_Form(forms.ModelForm):
    class Meta:
        model = Observation_Individual
        fields = ('client_location', 'client_homeless', 'client_age',
                  'client_gender', 'client_race', 'client_ethnicity', 'client_information',)


class Observation_Form(forms.ModelForm):
    class Meta:
        model = Observation

        # NOTE:
        # 1) The obs_user should be handled on our end (within views)
        # 2) The obs_householdnum is not user editable (as specified in models)
        fields = ('obs_reason', 'obs_adults', 'obs_children', 'obs_unsure',
                   'obs_client','obs_time', 'obs_user')

# Survey
# Individual
class Survey_Individual_Form(forms.ModelForm):
    class Meta:
        model = Survey_Individual
        fields = ('client_survey_initials', 'client_survey_relationship', 'client_survey_hhconfirm', 'client_survey_nonhhlastnight',
                  'client_survey_age_exact', 'client_survey_age_grouped', 'client_survey_ethnicity', 'client_survey_race',
                  'client_survey_race_other', 'client_survey_gender', 'client_survey_served', 'client_survey_served_guard_res',
                  'client_survey_served_VHA', 'client_survey_benefits', 'client_surey_firsttime' , 'client_survey_homelesslength',
                  'client_survey_homelesslength_number', 'client_survey_timeshomeless', 'client_survey_timeshomeless_length',
                  'client_survey_timeshomeless_number', 'client_survey_over18')

# Individual Extra

# Survey General
class Survey_Form(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('survey_lastnight', 'survey_repeat', 'survey_adults', 'survey_children',
                  'survey_client', 'survey_user')
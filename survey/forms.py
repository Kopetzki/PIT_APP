from django import forms

from .models import Observation_Individual, Observation

# WIP
class Observation_Individual_Form(forms.ModelForm):
    # define many to many

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

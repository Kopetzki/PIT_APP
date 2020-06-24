from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse

# import the different classes
from .models import Observation_Individual, Observation, Survey_Individual, Survey_IndividualExtra, Survey
from .forms import Observation_Individual_Form, Observation_Form, Survey_Individual_Form, Survey_Individual_Extra_Form, Survey_Form

# TO DO:
# Once the login is working, assign the author field to the user name of the current session
# Need to work on conditional formatting

# Create your views here.
# the survey index does nothing right now
def index(request):
    return HttpResponse("Hello, world. You're at the basic survey index.")

# ===================================================================
# Observation Individual
def observation_ind_detail(request, pk):
    obser = get_object_or_404(Observation_Individual, pk=pk)
    return render(request, 'observation/observation_ind_detail.html', {'obser': obser})

# Handles the form POST and GET
def observation_ind_new(request):
    if request.method == "POST":
        form = Observation_Individual_Form(request.POST)
        if form.is_valid():
            obs_ind = form.save() # Can add commit=False and save alter if need to add time/author/etc.
            # save many to many relationships correctly

            #print correctly
            print("pk: ", obs_ind.pk)
            print("client_location: ", obs_ind.client_location)
            print("homeless: ", obs_ind.client_homeless)

            return redirect('observation_ind_detail', pk=obs_ind.pk)
    else:
        # default w/o POST request: render the forms
        # will need an Observation form
        form = Observation_Individual_Form()
    return render(request, 'observation/obs_ind_form.html', {'form': form})

# ===================================================================
# General Observation
# WIP: Details need to be smoothed out
def observation_detail(request, pk):
    obser = get_object_or_404(Observation, pk=pk)
    return render(request, 'observation/observation_detail.html', {'obser': obser})

def general_observation(request):
    if request.method == "POST":
        form = Observation_Form(request.POST)
        if form.is_valid():
            obs = form.save()  # Can add commit=False and save alter if need to add time/author/etc.

            # TO DO: Need to add the obs_user field here with account management BEFORE saving
            # May also need to add "obs_householdnum"

            return redirect('observation_detail', pk=obs.pk)
    else:
        # default w/o POST request: render the forms
        # will need an Observation form
        form = Observation_Form()
    return render(request, 'observation/gen_obs.html', {'form': form})

# ===================================================================
# Survey Individual
def survey_ind_detail(request, pk):
    survey = get_object_or_404(Survey_Individual, pk=pk)
    return render(request, 'survey/survey_ind_detail.html', {'survey': survey})

def survey_ind_extra_detail(request, pk1 ,pk2):
    survey1 = get_object_or_404(Survey_Individual, pk=pk1)
    survey2 = get_object_or_404(Survey_IndividualExtra, pk=pk2)

    # pack two surveys into a dictionary
    surveys = {}
    surveys.update({'survey': survey1, 'survey2': survey2})

    return render(request, 'survey/survey_ind_extra_detail.html', surveys)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Survey Extra
# Needs to extend off the Individual survey above
# WIP

def survey_individual(request):
    if request.POST:
        form = Survey_Individual_Form(request.POST)

        #get age
        if form.is_valid():
            surv = form.save(commit=False)
            tempAge = surv.client_survey_age_exact
            print('tempAge:', tempAge)


        # client is over 18
        if tempAge >= 18:
            form_extra = Survey_Individual_Extra_Form(request.POST)

            if all([form.is_valid(), form_extra.is_valid()]):
                surv_extra = form_extra.save()

                # delay saving the individual form
                surv = form.save(commit=False)

                # assign the extra information to "client_survey_over18" variable
                surv.client_survey_over18 = surv_extra
                # now save the completed form
                surv.save()

                return redirect('survey_ind_extra_detail', pk1=surv.pk, pk2=surv_extra.pk)

        # client is younger than 18
        else:
            if form.is_valid():
                surv = form.save()  # Can add commit=False and save alter if need to add time/author/etc.

                return redirect('survey_ind_detail', pk=surv.pk)


    else:
        # default w/o POST request: render the forms
        form = Survey_Individual_Form()
        form_extra = Survey_Individual_Extra_Form()

        # pack two forms into a dictionary
        forms = {}
        forms.update({'form': form, 'form_extra': form_extra})

    return render(request, 'survey/survey_ind_form.html', forms)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Survey General
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    return render(request, 'survey/survey_detail.html', {'survey': survey})

# convert here
def survey_new(request):
    if request.method == "POST":
        form = Survey_Form(request.POST)
        if form.is_valid():
            surv = form.save()  # Can add commit=False and save alter if need to add time/author/etc.

            return redirect('survey_detail', pk=surv.pk)
    else:
        # default w/o POST request: render the forms
        form = Survey_Form()
    return render(request, 'survey/survey_form.html', {'form': form})


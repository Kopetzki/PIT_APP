from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse

# import the different classes
from .models import Observation_Individual, Observation
from .forms import Observation_Individual_Form, Observation_Form

# Create your views here.
# the survey index does nothing right now
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# ===================================================================
# Observation Individual
def observation_ind_detail(request, pk):
    obser = get_object_or_404(Observation_Individual, pk=pk)
    return render(request, 'survey/observation_ind_detail.html', {'obser': obser})

# To be deleted later; just for debugging
def obs_ind_list(request):
    observations = Observation_Individual.objects.order_by('pk')
    return render(request, 'survey/obs_ind_list.html', {'observations': observations})

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
    return render(request, 'survey/obs_ind_form.html', {'form': form})

# ===================================================================
# General Observation
# WIP: Details need to be smoothed out
def general_observation(request):
    if request.method == "POST":
        form = Observation_Form(request.POST)
        if form.is_valid():
            obs = form.save()  # Can add commit=False and save alter if need to add time/author/etc.

            # TO DO: Need to add the obs_user field here with account management BEFORE saving
            # May also need to add "obs_householdnum"

            return redirect('observation_ind_detail', pk=obs.pk)
    else:
        # default w/o POST request: render the forms
        # will need an Observation form
        form = Observation_Form()
    return render(request, 'survey/gen_obs.html', {'form': form})

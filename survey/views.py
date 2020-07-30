from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

# import the different classes
from .models import Observation_Individual, Observation, Survey_Individual, Survey_IndividualExtra, Survey, HOMELESS_CHOICES
from .forms import Observation_Individual_Form, Observation_Form, Survey_Individual_Form, Survey_Individual_Extra_Form, \
    Survey_Form, SignUpForm

# Create your views here.
# ===================================================================
# Basic Static Views
# ===================================================================
# Home
def index(request):
    return render(request, 'base/home1.html')
# Data dashboard
def dashboard(requests):
    return render(requests, 'data_dashboard/dashboard.html')
# Resources
def resources(request):
    return render(request, 'base/Resources.html')

# ===================================================================
# Observation Individual
# ===================================================================
@login_required
def observation_ind_detail(request, pk):
    obser = get_object_or_404(Observation_Individual, pk=pk)

    # get the special details of the form that requires more parsing
    raceList = obser.race_list

    # compact into dict
    data = {}
    data.update({'obser': obser, 'raceList': raceList})

    return render(request, 'observation/observation_ind_detail.html', data)

# Handles the form POST and GET; generate the observation individual form
# (+ some work in the HTML form) This works to attach users to the individual form
@login_required
def observation_ind_new(request):
    if request.method == "POST":
        form = Observation_Individual_Form(request.POST)
        if form.is_valid():
            #obs_ind = form.save()
            #"""
            obs_ind = form.save(commit=False)  # Can add commit=False and save alter if need to add time/author/etc.

            # Save username on backend based on who is logged in
            current_user = request.user
            print('user:', current_user.username)

            # attach the user to the form
            obs_ind.c_obs_user = current_user

            # now save the completed form
            obs_ind.save()
            form.save_m2m()  # for many to many fields, must save when commit=False is invoked

            """
            print("pk: ", obs_ind.pk)
            print("client_location: ", obs_ind.client_location)
            print("homeless: ", obs_ind.client_homeless)
            """

            return redirect('observation_ind_detail', pk=obs_ind.pk)
    else:
        # default w/o POST request: render the forms
        # will need an Observation form
        print("invalid")
        form = Observation_Individual_Form()

    return render(request, 'observation/obs_ind_form.html', {'form': form})

# ===================================================================
# General Observation
# ===================================================================
@login_required
def observation_detail(request, pk):
    obser = get_object_or_404(Observation, pk=pk)

    # get the special details of the form that requires more parsing
    o_reason = obser.get_obs_reason_display()
    o_clientList = obser.clients_list()

    # compact into dict
    data = {}
    data.update({'obser': obser, 'o_reason': o_reason, 'o_clientList': o_clientList})

    return render(request, 'observation/observation_detail.html', data)

@login_required
def general_observation(request):
    if request.method == "POST":
        form = Observation_Form(request.user, request.POST)
        if form.is_valid():
            #obs = form.save()
            obs = form.save(commit=False)  # Can add commit=False and save alter if need to add time/author/etc.

            # Save username on backend based on who is logged in
            print('user:', request.user.username)

            # attach the user (object) to the form
            obs.obs_user = request.user

            # now save the completed form
            obs.save()
            form.save_m2m()  # for many to many fields, must save when commit=False is invoked

            return redirect('observation_detail', pk=obs.pk)
    else:
        # default w/o POST request: render the forms

        # To do: Get the individuals  JUST submitted from their acct within the past few days
        # send that data into the html form
        print("invalid")

        # Call the form, but it is initialized with the user parameter to query based on logged in user
        form = Observation_Form(request.user)
    return render(request, 'observation/gen_obs.html', {'form': form})


# ===================================================================
# Survey Individual
# ===================================================================
@login_required
def survey_ind_detail(request, pk):
    survey = get_object_or_404(Survey_Individual, pk=pk)
    # get the special details of the form that requires more parsing
    raceList = survey.race_list()

    # Yes/No
    # Many to many
    hhconfirm = survey.get_client_survey_hhconfirm_display()
    ethnicity = survey.get_client_survey_ethnicity_display()
    served = survey.get_client_survey_served_display()
    guardRes = survey.get_client_survey_served_guard_res_display()
    vha = survey.get_client_survey_served_VHA_display()
    benefits = survey.get_client_survey_benefits_display()
    firstTime = survey.get_client_surey_firsttime_display() #misspelled

    # compact into dict
    data = {}
    data.update({'survey': survey, 'raceList': raceList, 'hhconfirm': hhconfirm, 'ethnicity':ethnicity,
                 'guardRes':guardRes, 'vha':vha, 'benefits':benefits,
                 'served':served, 'firstTime':firstTime})

    return render(request, 'survey/survey_ind_detail.html', data)


# ===================================================================
# Survey Extra
# Extends off the Individual survey above
# ===================================================================
def survey_ind_extra_detail(request, pk1 ,pk2):
    survey1 = get_object_or_404(Survey_Individual, pk=pk1)
    survey2 = get_object_or_404(Survey_IndividualExtra, pk=pk2)

    # get the special details of the form that requires more parsing
    # Many to many
    raceList = survey1.race_list()
    barriersList = survey2.barriers_list()

    # Yes/No
    hhconfirm = survey1.get_client_survey_hhconfirm_display()
    ethnicity = survey1.get_client_survey_ethnicity_display()
    served = survey1.get_client_survey_served_display()
    guardRes = survey1.get_client_survey_served_guard_res_display()
    vha = survey1.get_client_survey_served_VHA_display()
    benefits = survey1.get_client_survey_benefits_display()
    firstTime = survey1.get_client_surey_firsttime_display() #misspelled

    substance = survey2.get_client_survey_substance_display()
    mhealth = survey2.get_client_survey_mhealth_display()
    phealth = survey2.get_client_survey_phealth_display()
    stablehousing = survey2.get_client_survey_stablehousing_display()
    specialed = survey2.get_client_survey_specialed_display()
    HIVAIDS = survey2.get_client_survey_HIVAIDS_display()
    DV = survey2.get_client_survey_DV_display()

    # pack two surveys and data into a dictionary
    surveys = {}
    surveys.update({'survey': survey1, 'survey2': survey2, 'raceList':raceList, 'barriersList':barriersList,
                    'hhconfirm': hhconfirm, 'stablehousing':stablehousing, 'guardRes':guardRes, 'vha':vha,
                    'benefits':benefits,
                    'ethnicity':ethnicity, 'served':served, 'firstTime':firstTime, 'substance':substance,
                    'mhealth':mhealth, 'phealth':phealth, 'specialed':specialed, 'HIVAIDS':HIVAIDS, 'DV':DV})

    return render(request, 'survey/survey_ind_extra_detail.html', surveys)


# ===================================================================
# Survey Individual
# ===================================================================
@login_required
def survey_individual(request):
    if request.POST:
        form = Survey_Individual_Form(request.POST)

        # init
        tempAge = 0

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

                # Assign the user object to the survey
                surv.s_obs_user = request.user

                # now save the completed form
                surv.save()
                form.save_m2m() # for many to many fields, must save when commit=False is invoked

                return redirect('survey_ind_extra_detail', pk1=surv.pk, pk2=surv_extra.pk)

        # client is younger than 18
        else:
            if form.is_valid():
                # delay saving the individual form
                surv = form.save(commit=False)

                # Assign the user object to the survey
                surv.s_obs_user = request.user

                # now save the completed form
                surv.save()
                form.save_m2m()  # for many to many fields, must save when commit=False is invoked

                return redirect('survey_ind_detail', pk=surv.pk)


    else:
        # default w/o POST request: render the forms
        form = Survey_Individual_Form()
        form_extra = Survey_Individual_Extra_Form()

        # pack two forms into a dictionary
        forms = {}
        forms.update({'form': form, 'form_extra': form_extra})

    return render(request, 'survey/survey_ind_form.html', forms)

# ===================================================================
# Survey General
# ===================================================================
@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    # Need to get the client information to display on the front end

    # access the survey's client names
    client_nameList = survey.clients_list()

    print("client_nameList", client_nameList)

    return render(request, 'survey/survey_detail.html', ({'survey': survey, 'client_nameList':client_nameList}))

# convert here
@login_required
def survey_new(request):
    if request.method == "POST":
        form = Survey_Form(request.user, request.POST)
        if form.is_valid():
            # delay saving the individual form
            surv = form.save(commit=False)

            # Assign the user object to the survey
            surv.survey_user = request.user

            # now save the completed form
            surv.save()
            form.save_m2m()  # for many to many fields, must save when commit=False is invoked

            # Get the name(s) of surveyed client(s) to display on detail rendering
            #listClients = surv.survey_client
            #print("listClients", listClients)

            return redirect('survey_detail', pk=surv.pk, )
    else:
        # Call the form, but it is initialized with the user parameter to query based on logged in user
        form = Survey_Form(request.user)

    return render(request, 'survey/survey_form.html', {'form': form})

# ===================================================================
# User login, logout
# ===================================================================
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('user')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', context={"form": form})

def logout(request):
    auth.logout(request)

    # clear the existing messages for the logout messages log
    existing_messages = messages.get_messages(request)
    for message in existing_messages:
        # This iteration is necessary
        pass

    messages.info(request, "You've been logged out.")
    return redirect('/login')

# ===================================================================
# User views, register
# Landing page after login
# ===================================================================
@login_required
def user(request):
    return render(request, 'base/user/user1.html')


def register(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            user = f.save()
            # Give access to admin for all users in debug mode.
            if settings.DEBUG:
                user.is_staff = True
                user.is_superuser = True
                user.save()
            messages.success(request, 'Account created successfully, you can now login.')
            return redirect('login')
        else:
            messages.error(
                request,
                'Something is wrong with your username or password, check that they meet the requirements.')
            return redirect('register')

    else:
        f = SignUpForm()

    return render(request, 'registration/register.html', {'form': f})

# ===================================================================
# User My account profile
# ===================================================================
@login_required
def user_profile(request):
    """
    print(request.user.username)
    print(request.user.email)
    print(request.user.first_name)
    print(request.user.last_name)
    print(request.user.is_staff)
    """

    profile_username = request.user.username
    profile_email = request.user.email
    profile_fName = request.user.first_name
    profile_lName = request.user.last_name

    # To change later based on user groups
    if request.user.is_staff == True:
        profile_staff = "Approved"
    else:
        profile_staff = "Pending"

    # Compact info into user dict to send to the profile page
    userData = {}
    userData.update({'username': profile_username,
                 'email': profile_email,
                 'fName': profile_fName,
                 'lName': profile_lName,
                 'staff_status': profile_staff,
                 })

    return render(request, 'base/user/user_profile.html', {'userData': userData})


# Dependent functions
# Return the status from a multiple choice field (local to the model)
def get_readable_status(i, choice, obser, gen_obs_objects):
    # init
    temp_status = ''

    # Get the STATUS options
    reasons = obser._meta.get_field(choice).choices

    # Iterate through the options and correlate the reasons to the status index
    for a in range(len(reasons)):
        if gen_obs_objects[i].get(choice) == reasons[a][0]:
            # retrieve the human readable status
            temp_status = reasons[a][1]

            # once found, can break out of iteration
            break

    return temp_status

def get_re_indexed_models(name_model):
    inst = name_model
    new_model = []

    # based on the # of choice in the model, re-index the choices starting at 1
    for x in range(len(inst)):
        # start x at 0 because Django saves fk id's starting @ 1
        curr_tuple = (x+1, name_model[x][1])
        new_model.append(curr_tuple)

    return new_model


def get_readable_fk(i, choices_model, gen_obs_objects, field):
    # init
    temp_status = ''

    # Re-define model based on counting index of 1
    new_homeless_model = get_re_indexed_models(choices_model)

    # Iterate through the options and correlate the reasons to the status index
    for a in range(len(new_homeless_model)):
        # define the current field
        curr_field = gen_obs_objects[i].get(field)

        if curr_field == new_homeless_model[a][0]:
            # retrieve the human readable status
            temp_status = new_homeless_model[a][1]
            # once found, can break out of iteration
            break

    return temp_status

def get_gen_obs_ind(i, curr_id, curr_object, temp_obj, raw_objects):
    # 1) Change the "client homeless id" to be user readable (not the index, but the message)

    # method to get the readable data based on fk model ( stored with a "_id" at end)
    temp_status_client_homeless = get_readable_fk(i, HOMELESS_CHOICES, raw_objects, "client_homeless_id")

    # Append the change onto the object
    temp_obj.update(upd_client_homeless=temp_status_client_homeless)


    return temp_obj

def get_gen_obs(i, obser, temp_obs, gen_obs_objects):
    # 1) from that object, use the .clients_list method to get the clients
    curr_client_list = obser.clients_list()

    # update the temp object with the current client list
    temp_obs.update(clients=curr_client_list)

    # 2) Change the observation reason to be user readable (not the index, but the message)
    temp_status_obs_reason = get_readable_status(i, "obs_reason", obser, gen_obs_objects)

    # Update the list to include the readable reasons
    temp_obs.update(upd_obs_reason=temp_status_obs_reason)

    return temp_obs


def get_user_history_data(raw_objects, model_type, str_type):
    # init
    final_objects = []

    print(len(raw_objects))

    # iterate through the object list, and get the object with that primary key
    for i in range(len(raw_objects)):
        # get curr id based on the iteration we are in within object list
        curr_id = raw_objects[i].get("id")
        # print("id", curr_id)

        # get the corresponding object by pk id
        curr_object = get_object_or_404(model_type, pk=curr_id)

        # create a temp object based on the iteration
        temp_obj = raw_objects[i]

        # branch based on type of data
        if str_type == "Observation":
            temp_obj = get_gen_obs(i, curr_object, temp_obj, raw_objects)
        elif str_type == "Observation_Individual":
            temp_obj = get_gen_obs_ind(i, curr_id, curr_object, temp_obj, raw_objects)


        # add just an index to that object as well
        temp_obj.update(num=i)

        # append temp to a list
        final_objects.append(temp_obj)

    # Return
    return final_objects




# User History
@login_required
def user_history(request):
    # Query the different objects based on the user logged in
    # 1) Observation Individual Objects
    gen_obs_ind_objects = Observation_Individual.objects.all().filter(c_obs_user=request.user).values()

    print(gen_obs_ind_objects)

    # Call the method to parse the data to be user-readable
    # only do this if the length of the queried objects is greater than 1
    if len(gen_obs_ind_objects) >= 1:
        gen_obs_ind_objects_fin = get_user_history_data(gen_obs_ind_objects, Observation_Individual, "Observation_Individual")


    # 2) General Observation objects
    gen_obs_objects = Observation.objects.all().filter(obs_user=request.user).values()

    # Call the method to parse the data to be user-readable
    if len(gen_obs_objects) >= 1:
        gen_obs_objects_fin = get_user_history_data(gen_obs_objects, Observation, "Observation")


    #LATER: add the length of the returned objets so there is only a table if that user has submitted a form of that type
    # Split into 2 tabs: Observations and Surveys

    return render(request, 'base/user/user_history.html', ({'gen_obs_objects_fin': gen_obs_objects_fin,
                                                            'gen_obs_ind_objects_fin': gen_obs_ind_objects_fin}))
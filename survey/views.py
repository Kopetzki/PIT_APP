from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.db.models import Q

# import the different classes
from .models import Age, Observation_Individual, Observation, Survey_Individual, Survey_IndividualExtra, Survey, HOMELESS_CHOICES, \
    AGE_CHOICES, ETHNICITY_CHOICES, GENDER_CHOICES, LAST_NIGHT_CHOICES, YES_NO_CHOICES, RELATIONSHIP_CHOICES, \
    GENDER_DETAILED_CHOICES, HOMELESS_LENGTH_CHOICES, TIMES_HOMELESS_CHOICE, BARRIERS_CHOICES
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

            # Calculate the ages for the form based on individuals observed.
            ages = [ind.client_age for ind in form.cleaned_data['obs_client']]
            for age in ages:
                if age.age == 0:
                    obs.obs_children += 1
                elif age.age == 1 or age.age == 2:
                    obs.obs_adults += 1
                else:
                    obs.obs_unsure += 1

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

                # Derive age group from required exact age.
                if tempAge < 25:
                    surv.client_survey_age_grouped = Age.objects.get(age=1)
                else:
                    surv.client_survey_age_grouped = Age.objects.get(age=2)

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

                # Must be under 18 to take this branch.
                surv.client_survey_age_grouped = Age.objects.get(age=0)

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

            # Calculate the ages for the form based on individuals observed.
            ages = [ind.client_survey_age_exact for ind in form.cleaned_data['survey_client']]
            for age in ages:
                if age < 18:
                    surv.survey_children += 1
                else:
                    surv.survey_adults += 1

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
                return redirect('user_profile')
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
            # Put new users into Unapproved group
            # group = Group.objects.get(name='Unapproved Users')
            # user.groups.add(group)
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
    if request.user.groups.filter(name='Admin Users').exists():
        profile_staff = "Admin"
    elif request.user.groups.filter(name='Approved Users').exists():
        profile_staff = "Approved"
    elif request.user.groups.filter(name='Unapproved Users').exists():
        profile_staff = "Unapproved"
    else:
        profile_staff = "Unknown"

    # Compact info into user dict to send to the profile page
    userData = {}
    userData.update({'username': profile_username,
                 'email': profile_email,
                 'fName': profile_fName,
                 'lName': profile_lName,
                 'staff_status': profile_staff,
                 })

    return render(request, 'base/user/user_profile.html', ({'userData': userData}))


# User History
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

# Parse out yes or no based on 1/0 choice
def parse_yes_no(obj, field):
    val_field = obj.get(field)

    # Update the message field
    if val_field == 0:
        rep_upd = "No"
    elif val_field == 1:
        rep_upd = "Yes"
    else:
        rep_upd = "DK/REF"

    return rep_upd

# Parse yes/no on an object
def parse_yes_no_obj(field):
    # Update the message field
    if field == 0:
        rep_upd = "No"
    elif field == 1:
        rep_upd = "Yes"
    else:
        rep_upd = "DK/REF"

    return rep_upd

# Re-index a model of choices to correlate with how Django stuctures their form data
def get_re_indexed_models(name_model):
    inst = name_model
    new_model = []

    # based on the # of choice in the model, re-index the choices starting at 1
    for x in range(len(inst)):
        # start x at 0 because Django saves fk id's starting @ 1
        curr_tuple = (x+1, name_model[x][1])
        new_model.append(curr_tuple)

    return new_model

# Get the readable choice data from attributes with Foreign Key relationships to other models
def get_readable_fk(i, choices_model, gen_obs_objects, field):
    # init
    temp_status = ''

    # Re-define model based on counting index of 1
    new_model = get_re_indexed_models(choices_model)

    # Iterate through the options and correlate the reasons to the status index
    for a in range(len(new_model)):
        # define the current field
        curr_field = gen_obs_objects[i].get(field)

        if curr_field == new_model[a][0]:
            # retrieve the human readable status
            temp_status = new_model[a][1]
            # once found, can break out of iteration
            break

    return temp_status

# Specific fields needed for the observation individual
def get_gen_obs_ind_data(i, curr_id, curr_object, temp_obj, raw_objects):
    # 1) Change the "client homeless id" to be user readable (not the index, but the message)
    # method to get the readable data based on fk model ( stored with a "_id" at end)
    temp_status_client_homeless = get_readable_fk(i, HOMELESS_CHOICES, raw_objects, "client_homeless_id")
    # Append the change onto the object
    temp_obj.update(upd_client_homeless=temp_status_client_homeless)

    # 2) change the age choices
    temp_status_client_age = get_readable_fk(i, AGE_CHOICES, raw_objects, "client_age_id")
    # Append the change onto the object
    temp_obj.update(upd_client_age=temp_status_client_age)

    # 3) change the gender choices
    temp_status_client_gender = get_readable_fk(i, GENDER_CHOICES, raw_objects, "client_gender_id")
    # Append the change onto the object
    temp_obj.update(upd_client_gender=temp_status_client_gender)

    # 4) M2M Race Field (get via custom model method)
    curr_race_list = curr_object.race_list()
    # Append the change onto the object
    temp_obj.update(upd_client_race=curr_race_list)

    # 5) change the ethnicity choices
    temp_status_client_ethnicity = get_readable_fk(i, ETHNICITY_CHOICES, raw_objects, "client_ethnicity_id")
    # Append the change onto the object
    temp_obj.update(upd_client_ethnicity=temp_status_client_ethnicity)

    return temp_obj

# Specific fields needed for the general observation
def get_gen_obs_data(i, obser, temp_obs, gen_obs_objects):
    # 1) from that object, use the .clients_list method to get the clients
    curr_client_list = obser.clients_list()
    # update the temp object with the current client list
    temp_obs.update(clients=curr_client_list)

    # 2) Change the observation reason to be user readable (not the index, but the message)
    temp_status_obs_reason = get_readable_status(i, "obs_reason", obser, gen_obs_objects)
    # Update the list to include the readable reasons
    temp_obs.update(upd_obs_reason=temp_status_obs_reason)

    return temp_obs

# Specific fields needed for the survey
def get_survey_data(i, curr_object, temp_obj, raw_objects):
    # 1) change the last night choices
    temp_survey_lastnight = get_readable_fk(i, LAST_NIGHT_CHOICES, raw_objects, "survey_lastnight_id")
    # Append the change onto the object
    temp_obj.update(upd_survey_lastnight=temp_survey_lastnight)

    # 2) Repeat field: choices are hard coded in model Y/N
    rep_upd = parse_yes_no(raw_objects[i], "survey_repeat")
    # Update the list to include the readable reasons
    temp_obj.update(upd_survey_repeat=rep_upd)

    # 3) from that object, use the .clients_list method to get the clients
    curr_client_list = curr_object.clients_list()
    # update the temp object with the current client list
    temp_obj.update(clients=curr_client_list)

    return temp_obj

# Specific fields needed for the survey individual
def get_survey_ind_data(i, curr_object, temp_obj, raw_objects):
    # 1) change the relationship choices
    temp_s_relationship = get_readable_fk(i, RELATIONSHIP_CHOICES, raw_objects, "client_survey_relationship_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_relationship=temp_s_relationship)

    # 2) change the hhconfirm
    temp_s_hhconfirm = parse_yes_no(raw_objects[i], "client_survey_hhconfirm")
    # Append the change onto the object
    temp_obj.update(upd_s_i_hhconfirm=temp_s_hhconfirm)

    # 3) change the age choices
    temp_s_age_group = get_readable_fk(i, AGE_CHOICES, raw_objects, "client_survey_age_grouped_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_age_g=temp_s_age_group)

    # 4) change the ethnicity choices (Y/N)
    temp_s_ethnicity = parse_yes_no(raw_objects[i], "client_survey_ethnicity")
    # Append the change onto the object
    temp_obj.update(upd_s_i_ethnicity=temp_s_ethnicity)

    # 5) M2M Race Field (get via custom model method)
    curr_race_list = curr_object.race_list()
    # Append the change onto the object
    temp_obj.update(upd_s_i_race=curr_race_list)

    # 6) change the detailed gender
    temp_s_gender = get_readable_fk(i, GENDER_DETAILED_CHOICES, raw_objects, "client_survey_gender_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_gender=temp_s_gender)

    # 7) change the served choices (Y/N)
    temp_s_served = parse_yes_no(raw_objects[i], "client_survey_served")
    # Append the change onto the object
    temp_obj.update(upd_s_i_served=temp_s_served)

    # 8) change the firsttime choices (Y/N)
    temp_s_firsttime = parse_yes_no(raw_objects[i], "client_surey_firsttime")
    # Append the change onto the object
    temp_obj.update(upd_s_i_firsttime=temp_s_firsttime)

    # 9) change the homeless length
    temp_s_homeless_length= get_readable_fk(i, HOMELESS_LENGTH_CHOICES, raw_objects, "client_survey_homelesslength_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_homeless_length=temp_s_homeless_length)

    # 10) change the t homeless
    temp_s_t_homeless = get_readable_fk(i, TIMES_HOMELESS_CHOICE, raw_objects, "client_survey_timeshomeless_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_t_homeless=temp_s_t_homeless)

    # 11) change the t homeless length
    temp_s_t_homeless_length = get_readable_fk(i, HOMELESS_LENGTH_CHOICES, raw_objects, "client_survey_timeshomeless_length_id")
    # Append the change onto the object
    temp_obj.update(upd_s_i_t_homeless_length=temp_s_t_homeless_length)

    return temp_obj

# Specific fields needed for the survey individual extra
def get_survey_ind_extra_data(raw_objects):
    final_list = []

    # for every object, iterate through and change the fields to be human readable
    for i in range(len(raw_objects)):
        #make temp object empty dict
        temp_obj = {}

        # append the id
        temp_obj.update(id=raw_objects[i].pk)

        # 1) change the substance choices (Y/N)
        temp_s_e_substance = parse_yes_no_obj(raw_objects[i].client_survey_substance)
        # Append the change onto the object
        temp_obj.update(upd_s_e_substance=temp_s_e_substance)

        # 2) change the m health choices (Y/N)
        temp_s_e_mhealth = parse_yes_no_obj(raw_objects[i].client_survey_mhealth)
        # Append the change onto the object
        temp_obj.update(upd_s_e_mhealth=temp_s_e_mhealth)

        # 3) change the p health choices (Y/N)
        temp_s_e_phealth = parse_yes_no_obj(raw_objects[i].client_survey_phealth)
        # Append the change onto the object
        temp_obj.update(upd_s_e_phealth=temp_s_e_phealth)

        # 4) change the stable housing choices (Y/N)
        temp_s_e_stablehousing = parse_yes_no_obj(raw_objects[i].client_survey_stablehousing)
        # Append the change onto the object
        temp_obj.update(upd_s_e_stablehousing=temp_s_e_stablehousing)

        # 5) change the barriers list from custom model function
        barriers_list = raw_objects[i].barriers_list()
        temp_obj.update(upd_s_e_barriers_list=barriers_list)

        # 6) change the specialed(Y/N)
        temp_s_e_specialed = parse_yes_no_obj(raw_objects[i].client_survey_specialed)
        # Append the change onto the object
        temp_obj.update(upd_s_e_specialed =temp_s_e_specialed)

        # 7) change the client_survey_HIVAIDS(Y/N)
        temp_s_e_HIVAIDS = parse_yes_no_obj(raw_objects[i].client_survey_HIVAIDS)
        # Append the change onto the object
        temp_obj.update(upd_s_e_HIVAIDS=temp_s_e_HIVAIDS)

        # 8) change the client_survey_DV(Y/N)
        temp_s_e_DV = parse_yes_no_obj(raw_objects[i].client_survey_DV)
        # Append the change onto the object
        temp_obj.update(upd_s_e_DV=temp_s_e_DV)

        # append the current object to the final list
        final_list.append(temp_obj)

    return final_list

# A method to retrieve the user history data in a human readable way
# Generic for the 4 different forms
def get_user_history_data(raw_objects, model_type, str_type):
    # init
    final_objects = []

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
            temp_obj = get_gen_obs_data(i, curr_object, temp_obj, raw_objects)
        elif str_type == "Observation_Individual":
            temp_obj = get_gen_obs_ind_data(i, curr_id, curr_object, temp_obj, raw_objects)
        elif str_type == "Survey":
            temp_obj = get_survey_data(i, curr_object, temp_obj, raw_objects)
        elif str_type == "Survey_Individual":
            temp_obj = get_survey_ind_data(i, curr_object, temp_obj, raw_objects)
        else:
            print("Error: Invalid selection")

        # add just an index to that object as well
        temp_obj.update(num=i)

        # append temp to a list
        final_objects.append(temp_obj)

    # Return
    return final_objects

# Get the user ids of the surveyed clients over 18
def get_over_18_ids(survey_ind_objects):
    over_18_ids = []

    # First need to iterate through the survey individual objects, and retrieve if they have any over 18 (1-1)
    for i in range(len(survey_ind_objects)):
        # if the over 18 field is not none
        curr_over_18_field = survey_ind_objects[i].get("client_survey_over18_id")
        if curr_over_18_field != None:
            # then append it to the survey id list of the extra forms we need to display
            over_18_ids.append(curr_over_18_field)

    return over_18_ids

# Get the survey extra objects corresponding to the over 18 list
def get_surv_extra_objects(over_18_ids):
    # iterate through the Survey Individual Extra objects to get the objects with the matching pk ids
    # init
    surv_extra_objects = []

    # iterate through all the over_18 ids we need to retrieve
    for a in range(len(over_18_ids)):
        # get the corresponding Survey extra individual object
        curr_object = get_object_or_404(Survey_IndividualExtra, pk=over_18_ids[a])

        # add to final list
        surv_extra_objects.append(curr_object)

    return surv_extra_objects

# User History View with buttons
@login_required
def user_history(request):
    return render(request, 'base/user/user_history.html')

# User History for Observation Main View
@login_required
def user_history_obs(request):
    # init
    gen_obs_ind_objects_fin = ()
    gen_obs_objects_fin = ()

    # Query the different objects based on the user logged in
    # 1) Observation Individual Objects
    gen_obs_ind_objects = Observation_Individual.objects.all().filter(c_obs_user=request.user).values()

    # Call the method to parse the data to be user-readable
    # only do this if the length of the queried objects is greater than 1
    if len(gen_obs_ind_objects) >= 1:
        gen_obs_ind_objects_fin = get_user_history_data(gen_obs_ind_objects, Observation_Individual,
                                                        "Observation_Individual")

    # 2) General Observation objects
    gen_obs_objects = Observation.objects.all().filter(obs_user=request.user).values()

    # Call the method to parse the data to be user-readable
    if len(gen_obs_objects) >= 1:
        gen_obs_objects_fin = get_user_history_data(gen_obs_objects, Observation, "Observation")

    # Get the Length of the different forms query results
    g_obs_num = len(gen_obs_objects)
    obs_i_num = len(gen_obs_ind_objects)

    # check to see if there are no entries
    if g_obs_num == 0 and obs_i_num == 0:
        no_obs = True
    else:
        no_obs = False

    return render(request, 'base/user/user_history_obs.html',
                  ({'g_obs_num': g_obs_num, 'obs_i_num': obs_i_num, 'no_obs':no_obs,
                    'gen_obs_objects_fin': gen_obs_objects_fin,
                    'gen_obs_ind_objects_fin': gen_obs_ind_objects_fin,
                    }))


# User History for Survey Main View
@login_required
def user_history_surv(request):
    # init
    survey_ind_objects_fin = ()
    survey_objects_fin = ()
    survey_ind_extra_objects_fin = ()

    # Query the different objects based on the user logged in
    # 1) Survey Individual objects
    survey_ind_objects = Survey_Individual.objects.all().filter(s_obs_user=request.user).values()

    if len(survey_ind_objects) >= 1:
        survey_ind_objects_fin = get_user_history_data(survey_ind_objects, Survey_Individual, "Survey_Individual")

    # 2) Survey Individual Extra objects
    # call the method to get the over 18 ids from the current logged in user (derived from the "survey individual objects)
    over_18_ids = get_over_18_ids(survey_ind_objects)

    # Call the method to match the over 18 ids with the extra objects
    survey_ind_extra_objects = get_surv_extra_objects(over_18_ids)

    if len(survey_ind_extra_objects) >= 1:
        survey_ind_extra_objects_fin = get_survey_ind_extra_data(survey_ind_extra_objects)

    # 3) Survey objects
    survey_objects = Survey.objects.all().filter(survey_user=request.user).values()

    # Call the method to parse the data to be user-readable
    if len(survey_objects) >= 1:
        survey_objects_fin = get_user_history_data(survey_objects, Survey, "Survey")

    # Get the Length of the different forms query results
    surv_num = len(survey_objects)
    surv_i_num = len(survey_ind_objects)
    surv_e_num= len(survey_ind_extra_objects)

    # check to see if there are no entries
    if surv_num == 0 and surv_i_num == 0 and surv_e_num == 0:
        no_surv = True
    else:
        no_surv = False

    return render(request, 'base/user/user_history_surv.html',
                  ({'surv_num': surv_num, 'surv_e_num':surv_e_num,
                    'surv_i_num': surv_i_num, 'no_surv':no_surv,
                    'survey_objects_fin': survey_objects_fin,
                    'survey_ind_objects_fin': survey_ind_objects_fin,
                    'survey_ind_extra_objects_fin':survey_ind_extra_objects_fin,
                    }))
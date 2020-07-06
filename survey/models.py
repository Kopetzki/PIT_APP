from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

YES_NO_CHOICES = (
    (0, "No"),
    (1, "Yes"),
    (99, "DK/REF")
)

ETHNICITY_CHOICES = (
    (1, "Hispanic"),
    (2, "Non-Hispanic"),
    (99, "Doesn't Know"),
)

AGE_CHOICES = (
    (0, "Under 18"),
    (1, "18 - 24"),
    (2, "25+"),
    (99, "Not Sure"),
)

HOMELESS_CHOICES = (
    (0, 'Definetly'),
    (1, 'Possibly'),
    (99, 'Not Sure'),
)

GENDER_CHOICES = (
    (0, "Male"),
    (1, "Female"),
    (99, "Not Sure"),
)

GENDER_DETAILED_CHOICES = (
        (0, "Male"),
        (1, "Female"),
        (2, "Transgender"),
        (3, "Gender Non-Conforming(i.e., not exclusively male or female)"),
        (99, "Not Sure"),
)

RACE_CHOICES = (
    (0, "American Indian or Alaska Native"),
    (1, "Asian"),
    (2, "Black or African American"),
    (3, "Native Hawaiian or Other Pacific Islander"),
    (4, "White"),
    (5, "Other"),
    (99, "Not Sure")
)

LAST_NIGHT_CHOICES = (
        (1, "Street or sidewalk"),
        (2, "Vehicle (car, van, RV, truck)"),
        (3, "Park"),
        (4, "Abandoned building"),
        (5, "Bus, train station, airport"),
        (6, "Under bridge/overpass"),
        (7, "Woods or outdoor encampment"),
        (8, "Other location (specify)"),
        (9, "Emergency Shelter"),
        (10, "Transitional Housing"),
        (11, "Motel/Hotel"),
        (12, "House or apartment"),
        (13, "Jail, hospital, treatment program")
    )

YES_NO_DK_CHOICES = (
    (0, "No"),
    (1, "Yes"),
    (99, "DK/REF")
)

RELATIONSHIP_CHOICES = (
    (0, "Self"),
    (1, "Child"),
    (2, "Spouse"),
    (3, "Other Family"),
    (4, "Non-Married Partner"),
    (5, "Other, Non-Family")
)

HOMELESS_LENGTH_CHOICES = (
    (0, "Days"),
    (1, "Weeks"),
    (2, "Months"),
    (3, "Years"),
    (99, "DK/REF")
)

TIMES_HOMELESS_CHOICE= (
    (0, "Less than 4 times"),
    (1, "4 or more times"),
    (99, "DK/REF")
)

BARRIERS_CHOICES = (
    (0, "(a) Alcohol use/Illegal drug use"),
    (1, "(b) Psychiatric/emotional condition"),
    (2, "(c) Physical disability"),
    (3, "DK/REF")
)

class Ethnicity(models.Model):
    ethnicity = models.IntegerField(choices=ETHNICITY_CHOICES, default=1, null=True)

    def __str__(self):
        return self.get_ethnicity_display()


class Age(models.Model):
    age = models.IntegerField(choices=AGE_CHOICES, default=1, null=True)

    def __str__(self):
        return self.get_age_display()


class Homeless(models.Model):
    is_homeless = models.IntegerField(default=1, choices=HOMELESS_CHOICES, null=True)

    def __str__(self):
        return self.get_is_homeless_display()


class Gender(models.Model):
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, null=True)

    def __str__(self):
        return self.get_gender_display()


class GenderDetailed(models.Model):
    genderdetailed = models.IntegerField(choices=GENDER_DETAILED_CHOICES, default=1, null=True)

    def __str__(self):
        return self.get_genderdetailed_display()


class Race(models.Model):
    race = models.IntegerField(choices=RACE_CHOICES, default=1, null=True)

    def __str__(self):
        return self.get_race_display()


class LastNight(models.Model):
    lastnight = models.IntegerField(choices=LAST_NIGHT_CHOICES, default=1, null=False)

    def __str__(self):
        return self.get_lastnight_display()


class YesNoDK(models.Model):
    yesnodk = models.IntegerField(choices=YES_NO_DK_CHOICES, default=1, null=False)

    def __str__(self):
        return self.get_yesnodk_display()


class Relationship(models.Model):
    relationship = models.IntegerField(choices=RELATIONSHIP_CHOICES, default=0, null=False)

    def __str__(self):
        return self.get_relationship_display()


class HomelessLength(models.Model):
    homelesslength = models.IntegerField(choices=HOMELESS_LENGTH_CHOICES, default=2, null=False)

    def __str__(self):
        return self.get_homelesslength_display()


class TimesHomeless(models.Model):

    timeshomeless = models.IntegerField(choices=TIMES_HOMELESS_CHOICE, default=0, null=False)

    def __str__(self):
        return self.get_timeshomeless_display()

class Barriers(models.Model):
    barriers = models.IntegerField(choices=BARRIERS_CHOICES, default = 0, null=False)

    def __str__(self):
        return self.get_barriers_display()


class Observation_Individual(models.Model):
    client_location = models.CharField(max_length=200, help_text="Location where observed")
    client_homeless = models.ForeignKey(Homeless, on_delete=models.CASCADE)
    client_age = models.ForeignKey(Age, on_delete=models.CASCADE)
    client_gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    client_race = models.ManyToManyField(Race, help_text="Hold down \"Control\", or \"Command\" on a Mac, to select more than one.")
    client_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.CASCADE)
    client_information = models.CharField(max_length=200, help_text="Other information or identifying characteristics")

    def calc_race(self):
        if len(self.client_race.all()) > 1:
            return "Multi-Racial"
        else:
            return self.client_race.all().get()

    def __str__(self):
        return "ID: {} - ({}, {}, {})".format(self.pk, self.client_gender, self.client_age, self.calc_race())

    # client information
    def get_client(self):
        return "Client ID: {} - ({}, {}, {})".format(self.pk, self.client_gender, self.client_age, self.calc_race())

    # for query display results
    def race_list(self):
        return ', '.join([ind.get_race_display() for ind in self.client_race.all()])


class Observation(models.Model):
    STATUS = (
        (0, "You are unable to enter a site"),
        (1, "You cannot conduct a PIT count survey (person refused, language, or other problems"),
        (2, "You do not wish to disturb people sleeping")
    )
    obs_reason = models.IntegerField(choices=STATUS, default=1, null=True)
    obs_adults = models.IntegerField(default=0, null=True)
    obs_children = models.IntegerField(default=0, null=True)
    obs_unsure = models.IntegerField(default=0, null=True)
    obs_householdnum = models.IntegerField(editable=False, default=0, null=False)
    obs_client = models.ManyToManyField(Observation_Individual, help_text="Hold down \"Control\", or \"Command\" on a Mac, to select more than one.")
    obs_time = models.DateTimeField(default=timezone.now)
    obs_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.obs_householdnum = self.obs_adults + self.obs_children + self.obs_unsure
        super(Observation, self).save(*args, **kwargs)

    def __str__(self):
        return "ID: {} - Number in Household: {} - User: {}".format(self.pk, self.obs_householdnum, self.obs_user)

    # for query display results
    def clients_list(self):
        return ', '.join([ind.get_client() for ind in self.obs_client.all()])

#Only completed along Survey_Individual if the individual of the household is older than 18
class Survey_IndividualExtra(models.Model):
    client_survey_substance = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do you drink alcoholic beverages or use drugs\n(illegal or prescription for nonmedical reasons)?\n[IF NECESSARY: non-medical reasons means because of the experience or feeling the drug caused.]")
    client_survey_mhealth = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do you have psychiatric or emotional conditions such as depression or schizophrenia?")
    client_survey_phealth = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do you have a physical disability? This could include something that substantially limits one or more basic physical activities such as walking, climbing stairs, reaching, lifting, or carrying?")
    #If previous 3 questions were all NO or DK/REF, skip next 2 questions
    client_survey_stablehousing = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do any of the situations we just discussed keep you from holding a job or living in stable housing?")
    #if previous question was answered NO or DK/REF then skp next question
    client_survey_barriers = models.ManyToManyField(Barriers, help_text="Which ones keep you from holding a job or living in stable housing?")
    client_survey_specialed = models.IntegerField(choices=YES_NO_CHOICES, help_text="Have you ever received special education (or special ed.) services for an extended period of time?")
    client_survey_HIVAIDS = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do you have AIDS or an HIV-related illness?")
    client_survey_DV = models.IntegerField(choices=YES_NO_CHOICES, help_text="Are you experiencing homelessness because you are currently fleeing domestic violence, dating violence, sexual assault, or stalking?")

    # for query display results
    def barriers_list(self):
        return ', '.join([ind.get_barriers_display() for ind in self.client_survey_barriers.all()])


class Survey_Individual(models.Model):
    client_survey_initials = models.CharField(max_length = 25, help_text = "What are your initials?", null=True)
    client_survey_relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, help_text= "How are you related to the Head of Household (select 'Self' for the HoH)", null=True)
    #skip next two for the head of household, only for other people in household
    client_survey_hhconfirm = models.IntegerField(choices=YES_NO_CHOICES, help_text="Are you staying with this person tonight?", null=True)
    client_survey_nonhhlastnight = models.CharField(max_length = 100, help_text = "Where are you staying tonight?", null=True)
    client_survey_age_exact = models.IntegerField(help_text="How old are you? [ENTER NUMBER]", default=0, null=True)
    client_survey_age_grouped = models.ForeignKey(Age, on_delete=models.CASCADE, help_text= "[IF HESITANT ASK:] Are You?", null=True)
    client_survey_ethnicity = models.IntegerField(choices=YES_NO_CHOICES, help_text="Are you Hispanic or Latino?", null=True)
    client_survey_race = models.ManyToManyField(Race, help_text="What is your race? You can select one or more races.\n[READ CATEGORIES, DO NOT READ 'Please Specify.']")
    client_survey_race_other = models.CharField(max_length = 50, help_text="Please Specify.", null=True)
    client_survey_gender = models.ForeignKey(GenderDetailed, on_delete=models.CASCADE, help_text="What is your gender?", null=True)
    client_survey_served = models.IntegerField(choices=YES_NO_CHOICES, help_text="Have you served in the United States Armed Force\n(Army, Navy, Air Force, Marine Corps, or Coast Guard)?", null=True)
    #if previous question is NO, ask the next 2 questions, if YES or DK/REF skip the next 3
    client_survey_served_guard_res = models.IntegerField(choices=YES_NO_CHOICES, help_text = "Were you ever called into active duty\nas a member of the National Guard or as a Reservist? ", null=True)
    client_survey_served_VHA = models.IntegerField(choices=YES_NO_CHOICES, help_text="Have you ever received health care or benefits from a Veterans Administration medical center?", null=True)
    client_survey_benefits = models.IntegerField(choices=YES_NO_CHOICES, help_text="Do you receive any disability benefits such as\nSocial Security Income, Social Security Disability Income,\nor Veteran’s Disability Benefits?", null=True)
    client_surey_firsttime = models.IntegerField(choices=YES_NO_CHOICES, help_text="Is this the first time you have been homeless?", null=True)
    client_survey_homelesslength = models.ForeignKey(HomelessLength, on_delete=models.CASCADE, related_name="this_time", help_text="How long have you been homeless this time?\nOnly include time spent staying in shelters and/or on the streets.", null=True)
    client_survey_homelesslength_number = models.IntegerField(help_text="Enter number of days/weeks/months/Years:", null=True)
    #If client_survey_firsttime is YES skip the next two questions
    client_survey_timeshomeless = models.ForeignKey(TimesHomeless, on_delete=models.CASCADE, help_text="Including this time, how many times have you been homeless in the past 3 years?\nWas it 4 or more times or less than 4 times?", null=True)
    client_survey_timeshomeless_length = models.ForeignKey(HomelessLength, related_name="total_time", on_delete=models.CASCADE, help_text="If you add up all the times you have been homeless in the last 3 years,\nhow long have you been homeless? [ENTER DAYS OR WEEKS OR MONTHS OR YEARS]", null=True)
    client_survey_timeshomeless_number = models.IntegerField(help_text="Enter number of days/weeks/months/Years:", null=True)
    #following field only completed if individual older than 18
    client_survey_over18 = models.OneToOneField(Survey_IndividualExtra, on_delete=models.CASCADE, help_text="The next set of questions asks about sensitive topics. You don’t have to answer any question that you don’t\nwant to however your answers will be combined with the answers of other people who take the survey and\nused to help provide better programs and services to homeless people.", null=True)

    def __str__(self):
        return "ID: {} - Initials: {} - Age: {}".format(self.pk, self.client_survey_initials, self.client_survey_age_exact)

    # for query display results
    def race_list(self):
        return ', '.join([ind.get_race_display() for ind in self.client_survey_race.all()])


class Survey(models.Model):
    survey_lastnight = models.ForeignKey(LastNight, on_delete=models.CASCADE)
    survey_repeat = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1, null=False)
    survey_adults = models.IntegerField(default=0, null=True)
    survey_children = models.IntegerField(default=0, null=True)
    survey_householdnum = models.IntegerField(editable=False, default=0, null=False)
    survey_client = models.ManyToManyField(Survey_Individual, help_text="Hold down \"Control\", or \"Command\" on a Mac, to select more than one.")
    survey_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey_householdnum = self.survey_adults + self.survey_children
        super(Survey, self).save(*args, **kwargs)

    def __str__(self):
        return "ID: {} - Number in Household: {} - User: {}".format(self.pk, self.survey_householdnum, self.survey_user)


class SurveyCase(models.Model):
    survey_or_obs = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1, null=False)
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

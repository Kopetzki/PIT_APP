from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Ethnicity(models.Model):
    STATUS = (
        (1, "Hispanic"),
        (2, "Non-Hispanic"),
        (99, "Doesn't Know"),
    )
    ethnicity = models.IntegerField(choices=STATUS, default=1, null=True)

    def __str__(self):
        return self.get_ethnicity_display()


class Age(models.Model):
    STATUS = (
        (0, "Under 18"),
        (1, "18 - 24"),
        (2, "25+"),
        (99, "Not Sure"),
    )
    age = models.IntegerField(choices=STATUS, default=1, null=True)

    def __str__(self):
        return self.get_age_display()


class Homeless(models.Model):
    STATUS = (
        (0, 'Definetly'),
        (1, 'Possibly'),
        (99, 'Not Sure'),)
    is_homeless = models.IntegerField(default=1, choices=STATUS, null=True)

    def __str__(self):
        return self.get_is_homeless_display()


class Gender(models.Model):
    STATUS = (
        (0, "Male"),
        (1, "Female"),
        (99, "Not Sure"),
    )
    gender = models.IntegerField(choices=STATUS, default=1, null=True)

    def __str__(self):
        return self.get_gender_display()


class GenderDetailed(models.Model):
    STATUS = (
        (0, "Male"),
        (1, "Female"),
        (2, "Transgender"),
        (3, "Gender Non-Conforming(i.e., not exclusively male or female)"),
        (99, "Not Sure"),
    )

    genderdetailed = models.IntegerField(choices=STATUS, default=1, null=True)

    def __str__(self):
        return self.get_genderdetailed_display()


class Race(models.Model):
    STATUS = (
        (0, "American Indian or Alaska Native"),
        (1, "Asian"),
        (2, "Black or African American"),
        (3, "Native Hawaiian or Other Pacific Islander"),
        (4, "White"),
        (5, "Other"),
        (99, "Not Sure")
    )
    race = models.IntegerField(choices=STATUS, default=1, null=True)

    def __str__(self):
        return self.get_race_display()


class LastNight(models.Model):
    STATUS = (
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
    lastnight = models.IntegerField(choices=STATUS, default=1, null=False)

    def __str__(self):
        return self.get_lastnight_display()


class YesNoDK(models.Model):
    STATUS = (
        (0, "No"),
        (1, "Yes"),
        (99, "DK/REF")
    )

    yesnodk = models.IntegerField(choices=STATUS, default=1, null=False)

    def __str__(self):
        return self.get_yesnodk_display()


class Relationship(models.Model):
    STATUS = (
        (0, "Self"),
        (1, "Child"),
        (2, "Spouse"),
        (3, "Other Family"),
        (4, "Non-Married Partner"),
        (5, "Other, Non-Family")
    )

    relationship = models.IntegerField(choices=STATUS, default=0, null=False)

    def __str__(self):
        return self.get_relationship_display()


class HomelessLength(models.Model):
    STATUS = (
        (0, "Days"),
        (1, "Weeks"),
        (2, "Months"),
        (3, "Years"),
        (99, "DK/REF")
    )

    homelesslength = models.IntegerField(choices=STATUS, default=2, null=False)

    def __str__(self):
        return self.get_homelesslength_display()


class TimesHomeless(models.Model):
    STATUS = (
        (0, "Less than 4 times"),
        (1, "4 or more times"),
        (99, "DK/REF")
    )

    timeshomeless = models.IntegerField(choices=STATUS, default=0, null=False)

    def __str__(self):
        return self.get_timeshomeless_display()


class Observation_Individual(models.Model):
    client_location = models.CharField(max_length=200, help_text="Location where observed")
    client_homeless = models.ForeignKey(Homeless, on_delete=models.CASCADE)
    client_age = models.ForeignKey(Age, on_delete=models.CASCADE)
    client_gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    client_race = models.ManyToManyField(Race)
    client_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.CASCADE)
    client_information = models.CharField(max_length=200, help_text="Other information or identifying characteristics")

    def calc_race(self):
        if len(self.client_race.all()) > 1:
            return "Multi-Racial"
        else:
            return self.client_race.all().get()

    def __str__(self):
        return "ID: {} - ({}, {}, {})".format(self.pk, self.client_gender, self.client_age, self.calc_race())


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
    obs_client = models.ManyToManyField(Observation_Individual)
    obs_time = models.DateTimeField(default=timezone.now)
    obs_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.obs_householdnum = self.obs_adults + self.obs_children + self.obs_unsure
        super(Observation, self).save(*args, **kwargs)

    def __str__(self):
        return "ID: {} - Number in Household: {} - User: {}".format(self.pk, self.obs_householdnum, self.obs_user)


class Survey_Individual(models.Model):
    pass


class Survey(models.Model):
    survey_lastnight = models.ForeignKey(LastNight, on_delete=models.CASCADE)
    survey_adults = models.IntegerField(default=0, null=True)
    survey_children = models.IntegerField(default=0, null=True)
    survey_householdnum = models.IntegerField(editable=False, default=0, null=False)
    survey_client = models.ManyToManyField(Survey_Individual)
    survey_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey_householdnum = self.surey_adults + self.survey_children
        super(Survey, self).save(*args, **kwargs)

    def __str__(self):
        return "ID: {} - Number in Household: {} - User: {}".format(self.pk, self.survey_householdnum, self.survey_user)


class SurveyCase(models.Model):
    survey_or_obs = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1, null=False)
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

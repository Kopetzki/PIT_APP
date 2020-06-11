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


class Observation_Individual(models.Model):
    client_location = models.CharField(max_length=200, help_text="Location where observed")
    client_homeless = models.ForeignKey(Homeless, on_delete=models.CASCADE)
    client_age = models.ForeignKey(Age, on_delete=models.CASCADE)
    client_gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    client_race = models.ManyToManyField(Race)
    client_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.CASCADE)
    client_information = models.CharField(max_length=200, help_text="Other information or identifying characteristics")

    def __str__(self):
        return self.client_location

class Observation(models.Model):
    STATUS = (
        (0, "You are unable to enter a site"),
        (1, "You cannot conduct a PIT count survey (person refused, language, or other problems"),
        (2, "You do not wish to disturb people sleeping")
    )
    obs_reason = models.IntegerField(choices=STATUS, default =1, null=True)
    obs_adults = models.IntegerField(default=0, null = True)
    obs_children = models.IntegerField(default=0, null = True)
    obs_unsure = models.IntegerField(default=0, null = True)
    obs_client = models.ForeignKey(Observation_Individual, on_delete=models.CASCADE)
    obs_time = models.DateTimeField(default=timezone.now)
    obs_user = models.ForeignKey(User, on_delete=models.CASCADE)

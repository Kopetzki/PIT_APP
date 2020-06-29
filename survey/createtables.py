#from survey.models import Ethnicity, Age, Homeless, Gender, Race
from survey import models
from survey.models import LastNight, YesNoDK, Relationship, GenderDetailed, HomelessLength, TimesHomeless, Barriers

'''def create_tables():
    for x in Ethnicity.STATUS:
        Ethnicity.objects.create(ethnicity=x[0])
    for y in Age.STATUS:
        Age.objects.create(age=y[0])
    for z in Homeless.STATUS:
        Homeless.objects.create(is_homeless=z[0])
    for w in Gender.STATUS:
        Gender.objects.create(gender=w[0])
    for k in Race.STATUS:
        Race.objects.create(race=k[0])'''

def create_tables2():
    for x in models.LAST_NIGHT_CHOICES:
        LastNight.objects.create(lastnight=x[0])
    for y in models.YES_NO_DK_CHOICES:
        YesNoDK.objects.create(yesnodk=y[0])
    for z in models.RELATIONSHIP_CHOICES:
        Relationship.objects.create(relationship=z[0])
    for w in models.GENDER_DETAILED_CHOICES:
        GenderDetailed.objects.create(genderdetailed=w[0])
    for k in models.HOMELESS_LENGTH_CHOICES:
        HomelessLength.objects.create(homelesslength=k[0])
    for m in models.TIMES_HOMELESS_CHOICE:
        TimesHomeless.objects.create(timeshomeless=m[0])
    for n in models.BARRIERS_CHOICES:
        Barriers.objects.create(barriers=n[0])


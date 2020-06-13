#from survey.models import Ethnicity, Age, Homeless, Gender, Race
from survey.models import LastNight, YesNoDK, Relationship, GenderDetailed, HomelessLength, TimesHomeless

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
    for x in LastNight.STATUS:
        LastNight.objects.create(lastnight=x[0])
    for y in YesNoDK.STATUS:
        YesNoDK.objects.create(yesnodk=y[0])
    for z in Relationship.STATUS:
        Relationship.objects.create(relationship=z[0])
    for w in GenderDetailed.STATUS:
        GenderDetailed.objects.create(genderdetailed=w[0])
    for k in HomelessLength.STATUS:
        HomelessLength.objects.create(homelesslength=k[0])
    for m in TimesHomeless.STATUS:
        TimesHomeless.objects.create(timeshomeless=m[0])


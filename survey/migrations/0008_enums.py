from django.db import migrations

from survey import models


def forward(apps, schema_editor):
    Ethnicity = apps.get_model("survey", "Ethnicity")
    for c in models.ETHNICITY_CHOICES:
        Ethnicity.objects.create(ethnicity=c[0])
    Age = apps.get_model("survey", "Age")
    for c in models.AGE_CHOICES:
        Age.objects.create(age=c[0])
    Homeless = apps.get_model("survey", "Homeless")
    for c in models.HOMELESS_CHOICES:
        Homeless.objects.create(is_homeless=c[0])
    Gender = apps.get_model("survey", "Gender")
    for c in models.GENDER_CHOICES:
        Gender.objects.create(gender=c[0])
    Race = apps.get_model("survey", "Race")
    for c in models.RACE_CHOICES:
        Race.objects.create(race=c[0])
    LastNight = apps.get_model("survey", "LastNight")
    for c in models.LAST_NIGHT_CHOICES:
        LastNight.objects.create(lastnight=c[0])
    YesNoDK = apps.get_model("survey", "YesNoDK")
    for c in models.YES_NO_DK_CHOICES:
        YesNoDK.objects.create(yesnodk=c[0])
    Relationship = apps.get_model("survey", "Relationship")
    for c in models.RELATIONSHIP_CHOICES:
        Relationship.objects.create(relationship=c[0])
    GenderDetailed = apps.get_model("survey", "GenderDetailed")
    for c in models.GENDER_DETAILED_CHOICES:
        GenderDetailed.objects.create(genderdetailed=c[0])
    HomelessLength = apps.get_model("survey", "HomelessLength")
    for c in models.HOMELESS_LENGTH_CHOICES:
        HomelessLength.objects.create(homelesslength=c[0])
    TimesHomeless = apps.get_model("survey", "TimesHomeless")
    for c in models.TIMES_HOMELESS_CHOICE:
        TimesHomeless.objects.create(timeshomeless=c[0])
    Barriers = apps.get_model("survey", "Barriers")
    for c in models.BARRIERS_CHOICES:
        Barriers.objects.create(barriers=c[0])

def reverse(apps, schema_editor):
   pass


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20200623_1734'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
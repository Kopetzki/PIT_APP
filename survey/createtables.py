from survey.models import Ethnicity, Age, Homeless, Gender, Race


def create_tables():
    for x in Ethnicity.STATUS:
        Ethnicity.objects.create(ethnicity=x[0])
    for y in Age.STATUS:
        Age.objects.create(age=y[0])
    for z in Homeless.STATUS:
        Homeless.objects.create(is_homeless=z[0])
    for w in Gender.STATUS:
        Gender.objects.create(gender=w[0])
    for k in Race.STATUS:
        Race.objects.create(race=k[0])


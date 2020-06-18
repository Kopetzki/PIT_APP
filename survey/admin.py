from django.contrib import admin

# Register your models here.
from .models import Observation, Observation_Individual, Survey_IndividualExtra, Survey_Individual, Survey

admin.site.register(Observation)
admin.site.register(Observation_Individual)
admin.site.register(Survey)
admin.site.register(Survey_Individual)
admin.site.register(Survey_IndividualExtra)

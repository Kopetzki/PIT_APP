from django.contrib import admin

# Register your models here.
from .models import Observation, Observation_Individual

admin.site.register(Observation)
admin.site.register(Observation_Individual)
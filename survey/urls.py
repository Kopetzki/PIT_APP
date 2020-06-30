from django.urls import path, include

from . import views
from django.contrib import admin
from survey.dash_apps.finished_apps import main_dashboard

urlpatterns = [
    # Doesn't do anything now
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),

    path('resources/', views.resources, name='resources'),
    path('admin/', admin.site.urls),

    #for dashboard
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    # Individual Observations
    path('observation_ind_new/', views.observation_ind_new, name='observation_ind_new'),
    path('observation_ind_detail/<int:pk>/', views.observation_ind_detail, name='observation_ind_detail'),

    # General Observations
    path('observation_new/', views.general_observation, name='general_observation'),
    path('observation_detail/<int:pk>/', views.observation_detail, name='observation_detail'),


    # dashboard for graphs
    path('dashboard/', views.dashboard, name="dashboard"),

    # Survey Individual
    path('survey_ind_detail/<int:pk>/', views.survey_ind_detail, name='survey_ind_detail'),
    path('survey_new_ind/', views.survey_individual, name='survey_individual'),
    path('survey_ind_extra_detail/<int:pk1>/<int:pk2>/', views.survey_ind_extra_detail, name='survey_ind_extra_detail'),

    # Survey
    path('survey_detail/<int:pk>/', views.survey_detail, name='survey_detail'),
    path('survey_new/', views.survey_new, name='survey_new'),

]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views
from django.contrib import admin
from survey.dash_apps.finished_apps import main_dashboard


urlpatterns = [
    # Doesn't do anything now
    path('', views.index, name='index'),

    # User Views
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_history/', views.user_history, name='user_history'),
    path('user_history_obs/', views.user_history_obs, name='user_history_obs'),
    path('user_history_surv/', views.user_history_surv, name='user_history_surv'),

    path('resources/', views.resources, name='resources'),
    path('admin/', admin.site.urls),

    # for dashboard
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#        path('__debug__/', include(debug_toolbar.urls)),
#    ] + urlpatterns
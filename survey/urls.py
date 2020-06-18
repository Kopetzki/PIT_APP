from django.urls import path

from . import views

urlpatterns = [
    # Doesn't do anything now
    path('', views.index, name='index'),

    # Individual Observations
    path('observation_ind_new/', views.observation_ind_new, name='observation_ind_new'),
    path('observation_ind_detail/<int:pk>/', views.observation_ind_detail, name='observation_ind_detail'),
    path('observation_ind_list/', views.obs_ind_list, name='obs_ind_list'), # to be deleted

    # WIP: General Observations
    path('observation_new/', views.general_observation, name='general_observation'),
    path('observation_detail/<int:pk>/', views.observation_detail, name='observation_detail'),
]
"""PIT_APP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # User views
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user1/', views.user1, name='user1'),
    path('register/', views.register, name='register'),

    path('survey/', include('survey.urls')),
    path('resources/', views.resources, name='resources'),
    path('admin/', admin.site.urls),

    #for dashboard
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

    # will need another admin view for our custom dashboard

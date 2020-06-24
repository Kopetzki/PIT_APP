# Contains the main views of the application
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse

# import the different classes

# Create your views here.
def index(request):
    return render(request, 'base/home1.html')

def login(request):
    return render(request, 'registration/login.html')

def resources(request):
    return render(request, 'base/Resources.html')

# User views
# Landing page after login
def user1(request):
    return render(request, 'base/user/user1.html')
# Contains the main views of the application
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

# import the different classes

# Create your views here.


def index(request):
    return render(request, 'base/home.html')


def login(request):
    return render(request, 'base/login.html')


def resources(request):
    return render(request, 'base/Resources.html')


# User views
# Landing page after login
def user1(request):
    return render(request, 'base/user/user1.html')


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = UserCreationForm()

    return render(request, 'base/register.html', {'form': f})

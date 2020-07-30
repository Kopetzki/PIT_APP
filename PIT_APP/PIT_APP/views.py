# Contains the main views of the application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect


# import the different classes
# Create your views here.
def index(request):
    return render(request, 'base/home1.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('user1')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', context={"form": form})

def logout(request):
    auth.logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('/login')

def resources(request):
    return render(request, 'base/Resources.html')


# User views
# Landing page after login
@login_required
def user1(request):
    return render(request, 'base/user/user1.html')


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            # Put new users into Unapproved group
            # group = Group.objects.get(name='Unapproved Users')
            # user.groups.add(group)
            f.save()
            messages.success(request, 'Account created successfully, you can now login.')
            return redirect('login')
        else:
            messages.error(
                request,
                'Something is wrong with your username or password, check that they meet the requirements.')
            return redirect('register')

    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

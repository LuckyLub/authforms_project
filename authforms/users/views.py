from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='/users/login/')
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def register(request):
    """Register a new user."""

    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()

    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

    if form.is_valid():
        new_user = form.save()
        # Log the user in and then redirect to home page.
        authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
        login(request, authenticated_user)
        return HttpResponseRedirect(reverse('authforms_app:frontpage'))
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='/users/login/')
def profile(request):
    context = {}
    user = request.user
    context["user"] = user
    if "API-key" in request.POST:
        user.profile.api_key = request.POST["API-key"]
        user.save()

    if "topic" in request.POST:
        user.profile.topic = request.POST["topic"]
        user.save()

    return render(request, "profile.html", context)
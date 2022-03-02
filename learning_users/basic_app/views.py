from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# we have import more beacause we work lot of Django functionality
# Extra Imports for the Login and Logout Capabilities

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request,"index.html")

@login_required
def special(request):
    return HttpResponse("You logged in ")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):

    registered=False

    if request.method=="POST":

        user_form=UserForm(request.POST)
        profile_form=UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #first dealing with the user form
            user=user_form.save(commit=False)
            #this basically hashing the password(password is the field of class UserForm)
            #without setting password it will not store in data base

            user.set_password(user.password)

            #saving to the database

            user.save()

            #now dealing with profile_form

            profile=profile_form.save(commit=False)
            #set one to one relation between userform and profileform
            #we create one to one field in models.py

            profile.user=user

            #check if they provided a profile picture

            if 'profile_pic' in request.FILES:
                print("found it")
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,"registration.html",
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})



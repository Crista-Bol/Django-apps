from django.shortcuts import render
from fourth_app.forms import UserForm,UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):

    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
    {'registered':registered,'userform':user_form,'profileForm':profile_form})

def user_login(request):

    if request.method== 'POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        # Django's built-in authentication function
        user=authenticate(username=username,password=password)

        if user:
            # Check if user is active
            if user.is_active:
                # Log the user in
                login(request,user)

                # Send user to home page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is not active')
        else:
            print('Username: '+username)
            print('Password: '+password)
            return HttpResponse('Invalid login details supplied')

    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return render(request,'basic_app/login.html')

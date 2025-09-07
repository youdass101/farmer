from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from farmer.models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt



regcode = "123456"

# Create your views here.
#LOGIN PAGE 
def login_view(request):
    if request.method == "POST":
        # GET DATA
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)


        # IF AUTHENTICATION SUCCESS
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # IF AUTHENTICATION FAILED 
        else:
            return render(request, "user/login.html", {
                "error": "Invalid username or password.", "form": form
            }) 
    # GET METHOD TO LOAD LOGIN PAGE  
    else:
        if not request.user.is_authenticated:
            return render(request, "user/login.html", {"form": Login()})
        # IF USER IS ALREADY LOGGED IN LOAD INDEX PAGE 
        else:
            return HttpResponseRedirect(reverse("index"))


# LOGOUT FUNCTION 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# REGISTER NEW USER 
def register_view(request):
    if request.method == "POST":
        # GET CREDENTIALS 
        form =Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            comfirm = form.cleaned_data["confirm"]
            reg = form.cleaned_data["regcode"]
            # Check password and code
            if password == comfirm and reg == regcode:
                try:
                    new = User.objects.create_user(username, email, password)
                    new.save()
                except:
                    return render(request, "user/register.html", {"error": "user already exist", "form": form})
                
                # LOGIN WITH NEW USER 
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
            # ERROR
            else:
                return render(request, "user/register.html", {"error": "password comfirmation or REG Code do not match", "form": form})
        # MISSING CREDENTIALS
        else:
            return render(request, "user/register.html", {"error": "Missing Information"})    
    # GET PAGE 
    else:
        return render(request, "user/register.html", {"form": Register()})

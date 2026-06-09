from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError, transaction
from farmer.models import *
from .forms import *



regcode = "123456"

# LOGOUT FUNCTION 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Create your views here.
#LOGIN PAGE 
def login_view(request):
    if request.method == "POST":
        # GET DATA
        form = Login(request.POST)
        if not form.is_valid():
            return render(request, "user/login.html", {
                "error": "Enter a username and password.", "form": form
            }, status=400)

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


# REGISTER NEW USER 
def register_view(request):
    # subfunction to load page with error and form and load register page
    def registerpage(error, form):
        return render(request, "user/register.html", {"error": error, "form": form})
    # POST METHOD TO REGISTER NEW USER
    if request.method == "POST":
        # GET CREDENTIALS
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            comfirm = form.cleaned_data["confirm"]
            reg = form.cleaned_data["regcode"]
            # Check password and code
            if password == comfirm and reg == regcode:
                try:
                    with transaction.atomic():
                        User.objects.create_user(username, email, password)
                except IntegrityError:
                    return registerpage("user already exist", form)
                
                # LOGIN WITH NEW USER 
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
            # ERROR
            else:
                return registerpage("password comfirmation or REG Code do not match", form)
        # MISSING CREDENTIALS
        else:
            return registerpage("Missing Information", form)
    # GET PAGE 
    else:
        return registerpage("", Register())
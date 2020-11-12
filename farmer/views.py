from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import *

regcode = "123456"

# INDEX PAGE LOAD 
def index(request):
    if request.user.is_authenticated:
        return render (request, "farmer/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

#LOGIN PAGE 
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "farmer/login.html", {
                "message": "Invalid username or password."
            })  
    else:
        return render(request, "farmer/login.html")

# LOGOUT FUNCTION 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# REGISTER NEW USER 
def register_view(request):
    if request.method == "POST":
        try:

            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            comfirm = request.POST["confirm"]
            reg = request.POST["reg"]
            if password == comfirm and reg == regcode:
                try:
                    new = User.objects.create_user(username, email, password)
                    new.save()
                except:
                    return render(request, "farmer/register.html", {"error": "user already exist"})

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))

            else:
                return render(request, "farmer/register.html", {"error": "password comfirmation or REG Code do not match"})

        except:
            return render(request, "farmer/register.html", {"error": "Missing Information"})    
    
    else:
        return render(request, "farmer/register.html")
    

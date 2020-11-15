from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

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
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "farmer/login.html", {
                "error": "Invalid username or password.", "form": form
            })  
    else:
        return render(request, "farmer/login.html", {"form": Login()})

# LOGOUT FUNCTION 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# REGISTER NEW USER 
def register_view(request):
    if request.method == "POST":
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
                    return render(request, "farmer/register.html", {"error": "user already exist", "form": form})

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "farmer/register.html", {"error": "password comfirmation or REG Code do not match", "form": form})
        else:
            return render(request, "farmer/register.html", {"error": "Missing Information"})    
    else:
        return render(request, "farmer/register.html", {"form": Register()})

#plants view 
def plants(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        print(data)
        return None
        # form = Newplant(request.POST)
        # if form.is_valid():
        #     name = form.cleaned_data['name'].lower()
        #     seeds = form.cleaned_data['seeds']
        #     pressure = form.cleaned_data['pressure']
        #     blackout = form.cleaned_data['blackout']
        #     harvest = form.cleaned_data['harvest']
        #     output = form.cleaned_data['output']

            # newplant = Plant.objects.create(name=name, seeds=seeds, pressure=pressure, blackout=blackout, harvest=harvest, output=output)

    
    plantslist = Plant.objects.all()
    return render(request, "farmer/plants.html", {"form": Newplant(), "plants": plantslist})
    

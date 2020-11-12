from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render (request, "farmer/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
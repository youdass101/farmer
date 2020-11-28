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
from django.contrib.auth.decorators import login_required


regcode = "123456"

# INDEX PAGE LOAD 
def index(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            print("start here")
            form = json.loads(request.body)
            print("this is ",form)
            return True
        if request.method == "POST":
            form = Newtray(request.POST)
            if form.is_valid():
                name = form.cleaned_data['plant']
                medium = form.cleaned_data['medium']
                seed = form.cleaned_data['seed']
                medium_weight = form.cleaned_data['medium_weight']
                start = form.cleaned_data['start']
                count = form.cleaned_data['count']
                if not seed or seed == name.seeds:
                    seed = name.seeds 
                try: 
                    qtt = Tray.objects.filter(name=name).count()                   
                except:
                    qtt = 0
        
                for i in range(count):
                    c = qtt+i+1
                    Tray.objects.create(name=name, number= c, medium=medium, seeds_weight=seed, medium_weight=medium_weight, start=start)
                return HttpResponseRedirect(reverse("index"))
        
        sdata = Tray.objects.all()  
        data = [row.serialize() for row in sdata] 
        return render(request, "farmer/index.html", {"edit": Edittray(), "form": Newtray(), "data":data})
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
@login_required
def plants(request):
    if request.method == "POST":
        tp = json.loads(request.body)['type']
        if tp == "get":
            pp = json.loads(request.body)['data']
            data = Plant.objects.get(id=pp)
            print(data.seeds)
            return JsonResponse({"result": data.seeds}, status=201)

        
        if tp == "create":
            data = json.loads(request.body)['data']
            try:
                plant = Plant.objects.get(name=data['name'])
                return JsonResponse({"result": "exist"}, status=500)
            except:
                Plant.objects.create(name=data['name'].lower(), seeds=data['seeds'], pressure=data['pressure'], blackout=data['blackout'], harvest=data['harvest'], output=data['output'])
                return JsonResponse({"result": "done"}, status=201)
        
        if tp == "put":
            pp = json.loads(request.body)['data']
            edit = Plant.objects.get(id=pp['id'])
            if edit.name != pp['name']:
                try:
                    Plant.objects.get(name=pp['name'])
                    return JsonResponse({"msg":"Name already exist", "error": True}, status=206)
                except:
                    pas = True

            edit.name = pp['name']
            edit.seeds = pp['seeds']
            edit.pressure = pp['pressure']
            edit.blackout = pp['blackout']
            edit.harvest = pp['harvest']
            edit.output = pp['output']
            edit.save()
          
            return JsonResponse({"msg":"success", "error": False}, status=201)

        
    
    plantslist = Plant.objects.all()
    return render(request, "farmer/plants.html", {"form": Newplant(), "plants": plantslist})
    
# MEDIUM 
@login_required
def medium(request):
    if request.method == "POST":
        tp = json.loads(request.body)
        if tp['type'] == "create":
            try:
                Medium.objects.get(name=tp['data']['name'])
                return JsonResponse({"result": "exist"}, status=500)
            except:
                Medium.objects.create(name=tp['data']['name'].lower(), soil=tp['data']['soil'], coco=tp['data']['coco'])
                return JsonResponse({"result": "done"}, status=201)

        if tp['type'] == "put":
            print("it is put")
            print(tp['data']['id'])
            edit = Medium.objects.get(id=tp['data']['id'])
            print(edit)
            if edit.name != tp['data']['name']:
                try:
                    Medium.objects.get(name=tp['data']['name'])
                    return JsonResponse({"msg":"Name already exist", "error": True}, status=206)
                except:
                    pas = True
            edit.name = tp['data']['name']
            edit.soil = tp['data']['soil'] 
            edit.coco = tp['data']['coco']
            edit.save()
            return JsonResponse({"msg":"success", "error": False}, status=201)       

    mediumlist = Medium.objects.all()
    return render(request, "farmer/medium.html", {"form": Newmedium(), "data": mediumlist})

@login_required
def harvest(request):
    return None
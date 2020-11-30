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
            form = json.loads(request.body)
            if form['delete']:
                tray = Tray.objects.get(id=form['id'])
                tray.delete()
                return JsonResponse({"result": True, "msg": "Success"}, status=201)
            medium = Medium.objects.get(name=form["medium"])
            tray = Tray.objects.get(id=form['id'])
            tray.medium = medium
            tray.medium_weight = form['medium_weight']
            tray.seeds_weight = form['seed']
            tray.start = datetime.strptime(form['start'], '%b. %d, %Y')
            tray.save()
            return JsonResponse({"result": True, "msg": "Success"}, status=201)

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
                    print(name)
                    fname = name.name + str(c)
                    Tray.objects.create(name=name, fname=fname, number= c, medium=medium, seeds_weight=seed, medium_weight=medium_weight, start=start)
                return HttpResponseRedirect(reverse("index"))
        
        sdata = Tray.objects.all()
        data = [row.serialize() for row in sdata] 
        cd = str(datetime.date(datetime.today()))
        return render(request, "farmer/index.html", {"cd":cd, "edit": Edittray(), "form": Newtray(), "data":data})
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
        if not request.user:
            return render(request, "farmer/login.html", {"form": Login()})
        else:
            return HttpResponseRedirect(reverse("index"))


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
            edit = Medium.objects.get(id=tp['data']['id'])
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
    if request.method == "POST":
        form = json.loads(request.body)
        tray = Tray.objects.get(id=form['id'])
        Harvest.objects.create(tray=tray, date=form['d'], output=form['h'])
        return JsonResponse({"result": True, "msg": "Success"}, status=201)

@login_required
def history(request):
    sdata = Tray.objects.all()
    data = [row.serialize() for row in sdata] 
    return render(request, "farmer/history.html", {"data":data})

@login_required
def filter(request):
    if request.method == "POST":
        page = request.POST["page"]
        if page == "index":
            search = request.POST['search']
            if search != "":
                sdata = Tray.objects.filter(fname__contains=search)
                data = [row.serialize() for row in sdata]
            else:    
                filter = request.POST["filter"] 
                if filter == "name":
                    sdata = Tray.objects.all().order_by('name')
                    data = [row.serialize() for row in sdata] 
                else:
                    sdata = Tray.objects.all()
                    data = [row.serialize() for row in sdata]
                    data = sorted(data, key=lambda k: k[filter])
            cd = str(datetime.date(datetime.today()))
            return render(request, "farmer/index.html", {"cd":cd, "edit": Edittray(), "form": Newtray(), "data":data})
        elif page == "medium":
            filter = request.POST["filter"]
            data = Medium.objects.all().order_by(filter)
            return render(request, "farmer/medium.html", {"form": Newmedium(), "data": data})
        elif page == "plant":
            search = request.POST['search']
            if search != "":
                data = Plant.objects.filter(name__contains=search)
            else:
                filter = request.POST["filter"]
                data = Plant.objects.all().order_by(filter)
            return render(request, "farmer/plants.html", {"form": Newplant(), "plants": data})
        elif page == "history":
            search = request.POST['search']
            if search != "":
                sdata = Tray.objects.filter(fname__contains=search)
                data = [row.serialize() for row in sdata]
            else:
                filter = request.POST["filter"] 
                sdata = Tray.objects.all()
                data = [row.serialize() for row in sdata]
                data = sorted(data, key=lambda k: k[filter])
                 
            return render(request, "farmer/history.html", {"data":data})




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
import pandas as pd
from datetime import datetime
regcode = "123456"

# INDEX PAGE LOAD TRAYS 
def index(request):
    if request.user.is_authenticated:
        # GET DATA FROM JS 
        if request.method == "PUT":
            form = json.loads(request.body)
            # DELETE TRAY IF JS DATA DELETE IS TRUE 
            if form['delete']:
                tray = Tray.objects.get(id=form['id'])
                tray.delete()
                # RETURN STATUS AND MSG 
                return JsonResponse({"result": True, "msg": "Success"}, status=201)
            # EDIT TRAY FROM JS DATA IF DELET IS FLASE 
            medium = Medium.objects.get(name=form["medium"])
            tray = Tray.objects.get(id=form['id'])
            tray.medium = medium
            tray.medium_weight = form['medium_weight']
            tray.seeds_weight = form['seed']
            tray.start = datetime.strptime(form['start'], '%b. %d, %Y')
            return JsonResponse({"result": True, "msg": "Success"}, status=201)
        
        # CREATE NEW TRAY FROM HTML REQUEST
        if request.method == "POST":
            # GET NEW DATA FROM HTML FORM 
            form = Newtray(request.POST)
            # CHECK VALIDITY AND CLEAN FORM DATA 
            if form.is_valid():
                name = form.cleaned_data['plant']
                medium = form.cleaned_data['medium']
                seed = form.cleaned_data['seed']
                medium_weight = form.cleaned_data['medium_weight']
                start = form.cleaned_data['start']
                count = form.cleaned_data['count']
                location = form.cleaned_data['location']
                # IF SEED WEGHT IS NOT INSERTED 
                if not seed:
                    #DEFAULT SEEDS WEIGHT 
                    seed = name.seeds 
                try: 
                    # GET COUNT OF TRAY BASED ON PLANT NAME 
                    qtt = Tray.objects.filter(name=name).count()                   
                except:
                    # IF THIS IS THE FRIST TRAY OF IT KIND 
                    qtt = 0
                # CREATE NEW TRAY NUMBER
                for i in range(count):
                    # TRAY NUMBER BY NAME
                    c = qtt+i+1
                    # ADD NUMBER TO NAME 
                    fname = name.name + str(c)
                    # CREATE THE TRAY IN THE MODEL 
                    Tray.objects.create(name=name, fname=fname, number= c, medium=medium, seeds_weight=seed, medium_weight=medium_weight, start=start, location=location)
                return HttpResponseRedirect(reverse("index"))

        # GET METHOD TO LOAD PAGE WITH UPDATED DATA 
        # GET ALL CREATED TRAYS
        sdata = Tray.objects.all()
        # SERIALIZE EACH ROW WITH DETAILED DATA 
        data = [row.serialize() for row in sdata] 
        # GET ONLY ACTIVE NONE HARVEST TRAYS
        active = [x for x in data if not x["harvest"]]
        # GET TODAYS DATE 
        cd = str(datetime.date(datetime.today()))
        # SEND DATA TO HTML INDEX PAGE 
        return render(request, "farmer/index.html", {"cd":cd, "edit": Edittray(), "form": Newtray(), "data":active, "count":len(active)})
    # IF USER NOT LOGGED-IN REDIRECT TO LOGIN PAGE 
    else:
        return HttpResponseRedirect(reverse("login"))

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
            return render(request, "farmer/login.html", {
                "error": "Invalid username or password.", "form": form
            }) 
    # GET METHOD TO LOAD LOGIN PAGE  
    else:
        if not request.user.is_authenticated:
            return render(request, "farmer/login.html", {"form": Login()})
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
                    return render(request, "farmer/register.html", {"error": "user already exist", "form": form})
                
                # LOGIN WITH NEW USER 
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
            # ERROR
            else:
                return render(request, "farmer/register.html", {"error": "password comfirmation or REG Code do not match", "form": form})
        # MISSING CREDENTIALS
        else:
            return render(request, "farmer/register.html", {"error": "Missing Information"})    
    # GET PAGE 
    else:
        return render(request, "farmer/register.html", {"form": Register()})

# PLANTS 
@login_required
def plants(request):
    # CREATE PLANT
    if request.method == "POST":
        # LOAD JS TYPE NEST METHOD 
        tp = json.loads(request.body)['type']
        # NESTED GET SEEDS WEIGHT FOR AUTO ASSIGN IN FORM
        if tp == "get":
            pp = json.loads(request.body)['data']
            data = Plant.objects.get(id=pp)
            return JsonResponse({"result": data.seeds}, status=201)
        # CREATE NEW PLANT NESTED CREATE METHOD 
        if tp == "create":
            # LOAD DATA FROM JS TO CREATE NEW PLANT 
            data = json.loads(request.body)['data']
            try:
                # CHECK IF PLANT EXIST
                plant = Plant.objects.get(name=data['name'])
                return JsonResponse({"result": "exist"}, status=500)
            except:
                # CREATE NEW PLANT OBJECT INSTANCE 
                Plant.objects.create(name=data['name'].lower(), seeds=data['seeds'], pressure=data['pressure'], blackout=data['blackout'], harvest=data['harvest'], output=data['output'])
                # JAVA RESPONSE RETURN
                return JsonResponse({"result": "done"}, status=201)

        # EDIT OR UPDATE PLANT OBJECT INSTACNE 
        if tp == "put":
            # LOAD EDITED DATA FROM JS 
            pp = json.loads(request.body)['data']
            # LOAD EXISTING OBJECT BY ID
            edit = Plant.objects.get(id=pp['id'])
            # IF PLANT NAME EDITED AND CHANGED 
            if edit.name != pp['name']:
                try:
                    # CHECK IF NEW NAME ALREADY EXIST IF SO RETURN ERROR 
                    Plant.objects.get(name=pp['name'])
                    return JsonResponse({"msg":"Name already exist", "error": True}, status=206)
                except:
                    pass
            # UPDATE PLANT 
            edit.name = pp['name']
            edit.seeds = pp['seeds']
            edit.pressure = pp['pressure']
            edit.blackout = pp['blackout']
            edit.harvest = pp['harvest']
            edit.output = pp['output']
            edit.save()
            # RETURN SUCCESS 
            return JsonResponse({"msg":"success", "error": False}, status=201)

    # GET PAGE WITH ALL PLANTS TO LOAD THE PLANT PAGE 
    plantslist = Plant.objects.all()
    return render(request, "farmer/plants.html", {"form": Newplant(), "plants": plantslist})
    
# MEDIUM 
@login_required
def medium(request):
    if request.method == "POST":
        # LOAD DATA FROM JS
        tp = json.loads(request.body)
        # IF NESTED METHOD IS CREATE 
        if tp['type'] == "create":
            try:
                # CHECK IF MEDIUM NAME EXIST RETURN ERROR
                Medium.objects.get(name=tp['data']['name'])
                return JsonResponse({"result": "exist"}, status=500)
            except:
                # IF MEDIUM NAME DOESN'T EXIST CREATE NEW MEDIUM 
                Medium.objects.create(name=tp['data']['name'].lower(), soil=tp['data']['soil'], coco=tp['data']['coco'])
                return JsonResponse({"result": "done"}, status=201)
        # IF NESTED JS METHOD IS PUT 
        if tp['type'] == "put":
            # LOAD THE REQUEST MEDUIM MODEL OBJECT TO EDIT
            edit = Medium.objects.get(id=tp['data']['id'])
            # IF EDIT MEDIUM NAME CHANGED
            if edit.name != tp['data']['name']:
                try:
                    # CHECK IF NAME ALREADY EXIST IF YES RETURN ERROR
                    Medium.objects.get(name=tp['data']['name'])
                    return JsonResponse({"msg":"Name already exist", "error": True}, status=206)
                except:
                    pass
            # EDIT MEDIUM OBJECT DATA 
            edit.name = tp['data']['name']
            edit.soil = tp['data']['soil'] 
            edit.coco = tp['data']['coco']
            edit.save()
            return JsonResponse({"msg":"success", "error": False}, status=201)       
    # LOAD MEDIUM PAGE 
    mediumlist = Medium.objects.all()
    return render(request, "farmer/medium.html", {"form": Newmedium(), "data": mediumlist})

@login_required
def harvest(request):
    # HARVEST A TRAY ON REQUEST 
    if request.method == "POST":
        # GET HARVEST DATA FROM JS 
        form = json.loads(request.body)
        # GET TRAY MODEL OBJECT INSTANCE 
        tray = Tray.objects.get(id=form['id'])
        # CREATE HARVEST OBJECT IN HARVEST MODEL 
        Harvest.objects.create(tray=tray, date=form['d'], output=form['h'])
        return JsonResponse({"result": True, "msg": "Success"}, status=201)

@login_required
def history(request):
    # LOAD HISTORY PAGE 
    sdata = Tray.objects.all()
    # SERIALIZE HISTORY PAGE TRAYS DATA 
    fdata = [row.serialize() for row in sdata] 
    # FILTER ONLY HARVESTED TRAYS 
    data = [x for x in fdata if x["harvest"]]
    # SEND DATA TO HTML PAGE 
    return render(request, "farmer/history.html", {"data":data})

@login_required
def filter(request):
    if request.method == "POST":
        try:
            # REQUEST FILTER DATA 
            page = request.POST["page"]
            # INDEX PAGE TARGET 
            if page == "index":
                # SEARCH REQUEST STRING  
                search = request.POST['search']
                # SEARCH STRING IS NOT EMPTY 
                if search != "":
                    # SEARCH MODELS AND SERIALIZE 
                    sdata = Tray.objects.filter(fname__contains=search)
                    fdata = [row.serialize() for row in sdata]
                    
                else:    
                    # SEARCH STRING IS EMPTY REQUEST FILTER TARGET 
                    filter = request.POST["filter"] 
                    # FILTER IS BY NAME FILTER THE NAME AND SERIALIZE THEM 
                    if filter == "name":
                        sdata = Tray.objects.all().order_by('name')
                        fdata = [row.serialize() for row in sdata] 
                    else:
                        # IF FILTER IS ANYTHING ELSE THAN NAME SERIAL ALL DATA AND FILTER IT 
                        sdata = Tray.objects.all()
                        vdata = [row.serialize() for row in sdata]
                        fdata = sorted(vdata, key=lambda k: k[filter])
                # UPDATE DATE        
                cd = str(datetime.date(datetime.today()))
                # FILTER ACTIVE TRAYS 
                data = [x for x in fdata if not x["harvest"]]
                # RETURN FILTER DATA WITH NEEDE DEFAULT FORMS 
                return render(request, "farmer/index.html", {"cd":cd, "edit": Edittray(), "form": Newtray(), "data":data, "count": len(data)})
            # FILTER FROM MEDIUM PAGE 
            elif page == "medium":
                # REQUEST FILTER DATA 
                filter = request.POST["filter"]
                # LOAD ALL MEDIUMS MODELS AND FILTER THEM BY LOADED FILTER 
                data = Medium.objects.all().order_by(filter)
                return render(request, "farmer/medium.html", {"form": Newmedium(), "data": data})
            # FILTER PAGE IS PLANTS 
            elif page == "plant":
                # REQUEST SEARCH STRING
                search = request.POST['search']
                # IF SEARCH STRING IS NOT EMPTY 
                if search != "":
                    # SEARCH FOR STRING IN PLANTS MODEL
                    data = Plant.objects.filter(name__contains=search)
                else:
                    # IF SEARCH STRING IS EMPTY 
                    filter = request.POST["filter"]
                    # FILTER MODEL BY FILTER LOAD 
                    data = Plant.objects.all().order_by(filter)
                # RETURN FILTERED DATA 
                return render(request, "farmer/plants.html", {"form": Newplant(), "plants": data})
            # IF FILTER IS HISTORY PAGE 
            elif page == "history":
                # REQUEST SEARCH STRING FROM PAGE 
                search = request.POST['search']
                # IF SEARCH STRING IS NOT NONE
                if search != "":
                    # SEARCH AND SERIALIZE FILTER SEARCH 
                    sdata = Tray.objects.filter(fname__contains=search)
                    fdata = [row.serialize() for row in sdata]
                # IF SEARCH STRING IS NO NONE
                else:
                    # REQUEST FILTER FROM HTML PAGE 
                    filter = request.POST["filter"] 
                    # LOAD ALL TRAYS FROM MODEL 
                    sdata = Tray.objects.all()
                    # SERIALIZE ALL TRAYS 
                    vdata = [row.serialize() for row in sdata]
                    # FILTER ALL SERIALIZED DATA BY THE LOADED FILTER 
                    fdata = sorted(vdata, key=lambda k: k[filter])
                # REMOVE ACTIVE TRAYS AND LOAD ONLY HARVESTED TRAYS 
                data = [x for x in fdata if x["harvest"]]
                # RETURN ALL FILTERED DATA TO HISTORY PAGE 
                return render(request, "farmer/history.html", {"data":data})
        except:
            # FILTER ANALYTIC PAGE 
            dt = request.POST["start"]
            pname = request.POST["tray_name"]
            name = Plant.objects.get(name=pname.strip())
            sdata = Tray.objects.filter(name=name, start=datetime.strptime(dt, '%B %d, %Y'))
            print("here is success")
            vdata = [row.serialize() for row in sdata]
            data = [x for x in vdata if not x['harvest']]
            cd = str(datetime.date(datetime.today()))

            return render(request, "farmer/index.html", {"cd":cd, "edit": Edittray(), "form": Newtray(), "data":data, "count": len(data)})
         
# PAGE TO GROUP ACTIVE TRAYS BY NAME AND START DATE 
@login_required
def analytics(request):
    try:
        # LOAD ALL TRAYS OBJECTS 
        all = Tray.objects.all()
        # SERIALIZE MODELS 
        sall = [row.serialize() for row in all]
        # FILTER ACTIVE TRAYS AND REMOVE HARVESTED TRYAS 
        active = [x for x in sall if not x['harvest']]
        # CREATE A PANDA DICT FROM ACTIVE SERIALIZED TRAYS 
        pan = pd.DataFrame(active)
        # CONVER NAME TO STRING INSTEAD OF INSTANCE 
        pan = pan.astype({"name":str})
        # GROUP DADA BY NAME AND START DATE
        group = pan.groupby(['name', 'start', 'days', 'end'])
        # GET COUNT OF EACH GROUPED DATA BY NAME AND START 
        cn = pan.groupby(['name', 'start']).size().reset_index(name='cnt')
        # ZIP THE TOW PANDAS ARRAY TO ALIGN COUNT AND GROUPS 
        data = zip(group, cn.cnt)
    except:
        data = False
    # RETURN GROUPED DATA TO ANALYTIC PAGE 
    return render(request, "farmer/analytics.html", {"data":data, "form": Newtray() })



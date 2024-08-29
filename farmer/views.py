from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.aggregates import ArrayAgg

from .dfunctions.edititems import *


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime, timedelta
regcode = "123456"

# INDEX PAGE LOAD TRAYS 
@login_required
def index(request):
    if request.method == "GET":
        # GET ALL active CREATED TRAYS
        data = trayser("active")
        # SEND DATA TO HTML INDEX PAGE 
        return render(request, "farmer/index.html", {"cd":data["cd"], "form": Dnewtray(), "data":data["active"], "count":len(data["active"]), "harvestform": Nharvest })
    if request.method == "POST":
        # bulk delete by checkbox
        if request.POST["type"] == "bulkdelete":
            listdel = request.POST.getlist('dbid')
            for i in listdel:
                uitem = updateitem(({'type':'delete', 'poid': i}), Tray, Dnewmedium)
            return HttpResponseRedirect(reverse("index"))    

        if request.POST["type"] =="new":
            form = request.POST.copy()
            try: 
                # GET COUNT OF TRAY BASED ON PLANT NAME 
                qtt = Tray.objects.filter(name=form['name']).count() 
            except:
                # IF THIS IS THE FRIST TRAY OF IT KIND 
                qtt = 0
            # CREATE NEW TRAY NUMBER
            for i in range(int(form['count'])):
                # TRAY NUMBER BY NAME
                c =check_number(qtt, Tray, form['name'])
                # ADD NUMBER TO NAME 
                form.update({'number':c})
                uitem = updateitem(form, Tray, Dnewtray)
        else:
            uitem = updateitem(request.POST, Tray, Dnewtray)

        if uitem == True:
            return HttpResponseRedirect(reverse("index"))    
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})
        
        # Load edit form
        data = trayser("active")

        return render(request, "farmer/index.html", {"cd":data["cd"], "form": Dnewtray(), "data":data["active"], 
                                                     "count":len(data["active"]), "editform":uitem['editform'],})


# PLANTS 
@login_required
def plants(request):
    try: 
        # LOAD JS DATA 
        tp = json.loads(request.body)['type']
        # JS DATA FOR NEW TRAY CREATION 
        if tp == "fetch":
            pp = json.loads(request.body)['data']
            data = Plant.objects.get(id=pp)
             
            return JsonResponse({"result": [data.seeds, data.medium_weight]}, status=201)
    except:
        if request.method == "GET":
            plantslist = Plant.objects.all()
            return render(request, "farmer/plants.html", {"form": Dnewplant(), "data": plantslist})

        if request.method == "POST":
            uitem = updateitem(request.POST, Plant, Dnewplant)

        if uitem == True:
            return HttpResponseRedirect("plants")
        
        if uitem == False:
            return render(request, "farmer/plants.html",{"error": "SOMETHING WENT WRONG"})
        
        return render(request, "farmer/plants.html", uitem)
        

# MEDIUM PAGE 
@login_required
def medium(request):
    # LOADING DATA AND PAGE
    if request.method == "GET":
        mediumlist = Medium.objects.all()
        return render(request, "farmer/medium.html", {"form": Dnewmedium(), "data": mediumlist})
    
    # FETCH, EDIT, DELETE OBJECT
    if request.method == "POST":
        uitem = updateitem(request.POST, Medium, Dnewmedium)

    if uitem == True:
        return HttpResponseRedirect("medium")
    
    if uitem == False:
        return render(request, "farmer/medium.html",{"error": "SOMETHING WENT WRONG"})

    return render(request, "farmer/medium.html", uitem)


@login_required
def harvest(request):
    if request.method == "POST":
        uitem = updateitem(request.POST, Harvest, Nharvest)
        if uitem == True:
            return HttpResponseRedirect(reverse("index"))
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})            

  
    # # HARVEST A TRAY ON REQUEST 
    # if request.method == "POST":   
    #     # GET HARVEST DATA FROM JS 
    #     form = json.loads(request.body)  
    #     if form['bulk']:
    #         x = json.loads(form['tidl'])
    #         pack = Tray.objects.get(id=x[0])
    #         packweight = pack.name.packweight * int(form['hpw'])
    #         ttlweight = int(packweight) + int(form['hmw'])
    #         form['tidl'] = x 
    #         form['h'] = ttlweight / int(form['tqtt']) 
    #         ttlmed = pack.medium_weight * int(form['tqtt']) 
    #         ttlseed = pack.seeds_weight * int(form['tqtt'])
    #         mpercent = int(form['hmw']) / ttlweight
    #         ppercent = packweight / ttlweight

        

    #         BulkHarvest.objects.create(Product=pack.name, MediumMix=pack.medium, Trays=int(form['tqtt']), Harvestdate=form['d'], 
    #                            PacksQtt=int(form['hpw']), PacksWeight=packweight, MixWeight=int(form['hmw']), 
    #                            MediumWeightpacks= (ttlmed * ppercent), MediumWeightMix= (ttlmed * mpercent), SeedsWeightPacks= (ttlseed * ppercent),  SeedsWeightMix= (ttlseed*mpercent) )

        
    #     for i in range(int(form['tqtt'])):    
    #         # GET TRAY MODEL OBJECT INSTANCE 
    #         tray = Tray.objects.get(id=form['tidl'][i])
    #         # CREATE HARVEST OBJECT IN HARVEST MODEL 
    #         Harvest.objects.create(tray=tray, date=form['d'], output=form['h'])

    # return JsonResponse({"result": True, "msg": "Success"}, status=201)
        

@login_required
def history(request):
    if request.method == "GET":
        # LOAD HISTORY PAGE 
        sdata = Tray.objects.all()
        # SERIALIZE HISTORY PAGE TRAYS DATA 
        fdata = [row.serialize() for row in sdata] 
        # FILTER ONLY HARVESTED TRAYS 
        data = [x for x in fdata if x["harvest"]]
        # SEND DATA TO HTML PAGE 
        return render(request, "farmer/history.html", {"data":data})
    if request.method == "POST":

        if request.POST["type"] == "bulkdelete":
            listdel = request.POST.getlist('dbid')
            for i in listdel:
                updateitem({'type': 'delete', 'poid':i}, Harvest, Nharvest)
            return HttpResponseRedirect(reverse("history")) 

        uitem = updateitem(request.POST, Harvest, Nharvest)

        if uitem == True:
            return HttpResponseRedirect(reverse("history")) 
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})
        
        
        # load edit form
        data = trayser("inactive")
        return render(request, "farmer/history.html", {"data":data['active'],"editform":uitem["editform"] })



        





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
                return render(request, "farmer/plants.html", {"form": Dnewplant(), "plants": data})
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
        # filter only non harvested trays
        active = Tray.objects.exclude(id__in= Harvest.objects.values('tray'))
        # group trays my name and date
        grouped = active.values('name', 'start').annotate(qtt=models.Count('name'), seeds=models.Sum('seeds_weight'), soil=models.Sum('medium_weight'), list_id=ArrayAgg('id'))
        # create empty list to add data
        data=[]
         # TODAY DATE 
        today = datetime.today()
        todayu = str(datetime.date(datetime.today()))
        for v in grouped:
            data.append({'name': Plant.objects.get(id=v['name']).name, 
                            'start': datetime.date(v['start']), 'quantity': v['qtt'], 
                        'end':datetime.date(v['start']) + timedelta(Plant.objects.get(id=v['name']).harvest),
                        'days':datetime.date(today) - datetime.date(v['start']),
                        'seeds': v['seeds'], 
                        'soil': v['soil'],
                        'listid': v['list_id'],
                        'today': str(datetime.date(datetime.today()))})
    except:
        data = False
    # RETURN GROUPED DATA TO ANALYTIC PAGE 
    return render(request, "farmer/analytics.html", {"data":data, "form": Dnewtray(), "todayu": todayu })


@login_required
def report(request):
    if request.method == "GET":
        allbulk  = BulkHarvest.objects.all()[:10]
        data = [row.serialize() for row in  allbulk]
        filter = None  
        medium = 0
        totalyield = 0 
        reportfilter = None

    else:
        form = Reportfilter(request.POST)
        if form.is_valid():
            
            type = form.cleaned_data['type']
            productname = form.cleaned_data['product']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            medium = 0
            totalyield = 0
            reportfilter = Reportfilter()
            reportfilter.initial['type'] = type
            reportfilter.initial['product'] = productname
            reportfilter.initial['start'] = start
            reportfilter.initial['end'] = end
            filter = {'type': type, 'product': productname, 'start':start, 'end':end}
            if type=="All":
                
                filter = {'type': type, 'product': productname, 'start':start, 'end':end}
                if not productname:
                    allbulk = BulkHarvest.objects.filter(Harvestdate__range=[start, end])
                else:
                    allbulk = BulkHarvest.objects.filter(Product= productname, Harvestdate__range=[start, end])

                data = [row.serialize() for row in  allbulk]
                

            if type=="Packs":
                if not productname:
                    allbulk = BulkHarvest.objects.filter(Harvestdate__range=[start, end])
                    
                 
                else:
                    allbulk = BulkHarvest.objects.filter(Product= productname, Harvestdate__range=[start, end])
            
                data = [row.serialize() for row in  allbulk]

            if type=="Mix":
                if not productname:
                    allbulk = BulkHarvest.objects.filter(Harvestdate__range=[start, end])
                    for i in allbulk:
                        medium = medium + i.MediumWeightMix
                        totalyield = totalyield + i.MixWeight
                    
                 
                else:
                    allbulk = BulkHarvest.objects.filter(Product= productname, Harvestdate__range=[start, end])
                    for i in allbulk:
                        medium = medium + i.MediumWeightMix
                        totalyield = i.MixWeight
                    
            
                data = [row.serialize() for row in  allbulk]


             
    return render(request, "farmer/report.html", {"data": data, "fform": Reportfilter, "filter": filter, "medium": medium, "totalyield":totalyield, "rff": reportfilter})


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

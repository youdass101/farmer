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

import ast


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
        return render(request, "farmer/index.html", {"cd":data["cd"], "form": Dnewtray(),
                                                      "data":data["active"], "count":len(data["active"]),
                                                        "harvestform": Nharvest })
    if request.method == "POST":
        # bulk delete by checkbox
        if request.POST["type"] == "bulkdelete":
            listdel = request.POST.getlist('dbid')
            for i in listdel:
                uitem = updateitem(({'type':'delete', 'id': i}), Tray, Dnewmedium)
            return HttpResponseRedirect(reverse("index"))    

        # Create new Tray
        if request.POST["type"] =="new":
            uitem = newobject(request.POST.copy(), Tray, Dnewtray)
        # Filter Active trays by something
        elif request.POST["type"] == "filter":
            filter = request.POST
            data = filter_tray(Tray, filter, "active")
            return render(request, "farmer/index.html", {"cd":data["cd"], "form": Dnewtray(),
                                                      "data":data["active"], "count":len(data["active"]),
                                                        "harvestform": Nharvest })
            
        # Edit, fetch data or delete
        else:
            uitem = updateitem(request.POST, Tray, Dnewtray)

        if uitem == True:
            return HttpResponseRedirect(reverse("index"))    
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})

        
        # Load edit form
        data = trayser("active")

        return render(request, "farmer/index.html", {"cd":data["cd"], "form": Dnewtray(), "data":data["active"], 
                                                     "count":len(data["active"]), "editform":uitem['editform'],
                                                     "harvestform": Nharvest})


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
            if request.POST['type'] == "filter":
                data = filter_data(Plant, request.POST)
                return render(request, "farmer/plants.html", {"form": Dnewplant(), "data": data})

            else:
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
        if request.POST['type'] == "filter":
                data = filter_data(Medium, request.POST)
                return render(request, "farmer/medium.html", {"form": Dnewmedium(), "data": data})
      
        else:
            uitem = updateitem(request.POST, Medium, Dnewmedium)

    if uitem == True:
        return HttpResponseRedirect("medium")
    
    if uitem == False:
        return render(request, "farmer/medium.html",{"error": "SOMETHING WENT WRONG"})

    return render(request, "farmer/medium.html", uitem)


@login_required
def harvest(request):
    if request.method == "POST":
        form = request.POST.copy()

        if form['type'] == "bulknew":
            listid = ast.literal_eval(form['id'])
            tray = Tray.objects.get(id=listid[0])
            form.update({'Product': tray.name.id, 'MediumMix': tray.medium.id})
            nitem = Nbulkharvest(form)
            if nitem.is_valid():
                nitem = nitem.save()
            
            outp = (nitem.PacksWeight + nitem.MixWeight) / len(listid)
            for i in range(nitem.Trays):
                tray = Tray.objects.get(id=listid[i])         
                formd = Harvest(tray=tray, date=nitem.Harvestdate,
                                  output = outp, bulkh= nitem)
                formd.save()
             
            return HttpResponseRedirect(reverse("analytics"))

        uitem = updateitem(request.POST, Harvest, Nharvest)
        if uitem == True:
            return HttpResponseRedirect(reverse("index"))
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})            
    

@login_required
def history(request):
    if request.method == "GET":
        # # LOAD HISTORY PAGE 
        data = trayser("Inactive")
        # SEND DATA TO HTML PAGE 
        return render(request, "farmer/history.html", {"data":data['active']})
    if request.method == "POST":

        if request.POST["type"] == "bulkdelete":
            listdel = request.POST.getlist('dbid')
            for i in listdel:
                updateitem({'type': 'delete', 'id':i}, Harvest, Nharvest)
            return HttpResponseRedirect(reverse("history")) 
        elif request.POST["type"] == "filter":
            filter = request.POST
            data = filter_tray(Tray, filter, "inactive")
            return render(request, "farmer/history.html", {"data":data['active']})

        uitem = updateitem(request.POST, Harvest, Nharvest)

        if uitem == True:
            return HttpResponseRedirect(reverse("history")) 
        if uitem == False:
            return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"})
        
        # load edit form
        data = trayser("inactive")
        return render(request, "farmer/history.html", {"data":data['active'],"editform":uitem["editform"] })



# PAGE TO GROUP ACTIVE TRAYS BY NAME AND START DATE 
@login_required
def analytics(request):
    # TODAY DATE 
    todayu = str(datetime.date(datetime.today()))

    if request.method == "GET":
        data = groupingtrays()
        # RETURN GROUPED DATA TO ANALYTIC PAGE 
        return render(request, "farmer/analytics.html", {"data":data, "form": Dnewtray(), "todayu": todayu, "bulkharvest":Nbulkharvest })
    
    if request.method == "POST":
        if request.POST["type"]=="new":
            uitem = newobject(request.POST.copy(), Tray, Dnewtray)
        
        elif request.POST["type"]=="loadedit":
            list = ast.literal_eval(request.POST['itemid'])
            data = {"type": request.POST["type"] ,"itemid": list[0]}
            uitem = updateitem(data, Tray, Dnewtray, len(list))
            # filter only non harvested trays
            data = groupingtrays()

            return render(request, "farmer/analytics.html", {"data":data,"editform": uitem["editform"],
                                                              "form": Dnewtray(), "todayu": todayu, "bulkharvest":Nbulkharvest })
        else:
            req = request.POST.copy()
            object = Tray.objects.get(id=req['id'])
            count = int(req['count'])
            listobject = Tray.objects.filter(name=object.name, start=object.start)
            for i in listobject:
                if count == 0:
                    break
                else:
                    count -= 1
                    req.update({'id':i.id})
                    uitem = updateitem(req, Tray, Dnewtray)

        if uitem == True:
            return HttpResponseRedirect(reverse("analytics"))    
        if uitem == False:
            return render(request, "farmer/analytics.html",{"error": "SOMETHING WENT WRONG"}) 




@login_required
def report(request):
    medium = 0
    totalyield = 0 
    if request.method == "GET":
        allbulk  = BulkHarvest.objects.all()[:10]
        filter = None  
        form = None

    else:
        if request.POST['type'] == "delete":
            ditem = updateitem(request.POST, BulkHarvest, Nbulkharvest)
            if ditem == True:
                return HttpResponseRedirect(reverse("report"))    
            if ditem == False:
                return render(request, "farmer/reports.html",{"error": "SOMETHING WENT WRONG"}) 

        form = Reportfilter(request.POST)
        if form.is_valid():            
            type = form.cleaned_data['type']
            productname = form.cleaned_data['product']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            filter = {'type': type, 'product': productname, 'start':start, 'end':end}
            
            if not productname:
                allbulk = BulkHarvest.objects.filter(Harvestdate__range=[start, end])
            else:
                allbulk = BulkHarvest.objects.filter(Product= productname, Harvestdate__range=[start, end])
            

            if type=="Mix":
                if not productname:
                    for i in allbulk:
                        medium = medium + i.MediumWeightMix
                        totalyield = totalyield + i.MixWeight
                else:
                    for i in allbulk:
                        medium = medium + i.MediumWeightMix
                        totalyield = i.MixWeight

    data = [row.serialize() for row in  allbulk]

                    
    return render(request, "farmer/report.html", {"data": data, "fform": Reportfilter, "filter": filter, 
                                                  "medium": medium, "totalyield":totalyield, "rff": form})


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

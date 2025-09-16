from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .dfunctions.edititems import *
import ast
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime

# INDEX PAGE LOAD TRAYS 

def traylist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "GET":
            # GET ALL active CREATED TRAYS
            data = trayser("active")
            # SEND DATA TO HTML INDEX PAGE
            return render(request, "farmer/traylist.html", {"cd":data["cd"], "form": Dnewtray(),
                                                      "data":data["active"], "count":len(data["active"]),
                                                        "harvestform": Nharvest })
        if request.method == "POST":
            print("in POST")
            # bulk delete by checkbox
            if request.POST["type"] == "bulkdelete":
                listdel = request.POST.getlist('dbid')
                for i in listdel:
                    uitem = updateitem(({'type':'delete', 'id': i}), Tray, Dnewmedium)
                return HttpResponseRedirect(reverse("traylist"))    

            # Create new Tray
            if request.POST["type"] =="new":
                uitem = newobject(request.POST.copy(), Tray, Dnewtray)
            # Filter Active trays by something
            elif request.POST["type"] == "filter":
                print("in filter")
                filter = request.POST
                data = filter_tray(Tray, filter, "active")
                return render(request, "farmer/traylist.html", {"cd":data["cd"], "form": Dnewtray(),
                                                        "data":data["active"], "count":len(data["active"]),
                                                            "harvestform": Nharvest })
                
            # Edit, fetch data or delete
            else:
                uitem = updateitem(request.POST, Tray, Dnewtray)

            if uitem == True:
                return HttpResponseRedirect(reverse("index"))    
            if uitem == False:
                return render(request, "farmer/traylist.html",{"error": "SOMETHING WENT WRONG"})

            
            # Load edit form
            data = trayser("active")

            return render(request, "farmer/traylist.html", {"cd":data["cd"], "form": Dnewtray(), "data":data["active"], 
                                                        "count":len(data["active"]), "editform":uitem['editform'],
                                                        "harvestform": Nharvest})

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        # TODAY DATE 
        todayu = str(datetime.date(datetime.today()))

        if request.method == "GET":
            data = groupingtrays()
            # RETURN GROUPED DATA TO ANALYTIC PAGE 
            return render(request, "farmer/index.html", {"data":data, "form": Dnewtray(), "todayu": todayu, "bulkharvest":Nbulkharvest })
        
        if request.method == "POST":
            if request.POST["type"]=="new":
                uitem = newobject(request.POST.copy(), Tray, Dnewtray)
            
            elif request.POST["type"]=="loadedit":
                list = ast.literal_eval(request.POST['itemid'])
                data = {"type": request.POST["type"] ,"itemid": list[0]}
                uitem = updateitem(data, Tray, Dnewtray, len(list))
                # filter only non harvested trays
                data = groupingtrays()

                return render(request, "farmer/index.html", {"data":data,"editform": uitem["editform"],
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
                return HttpResponseRedirect(reverse("index"))    
            if uitem == False:
                return render(request, "farmer/index.html",{"error": "SOMETHING WENT WRONG"}) 

        


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
            plantslist = Plant.objects.filter(active=True)
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
             
            return HttpResponseRedirect(reverse("index"))

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



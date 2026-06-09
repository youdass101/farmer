from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .dfunctions.bulkharvest import BulkHarvestValidationError, create_bulk_harvest
from .dfunctions.edititems import *
import ast
from .models import *
from .forms import *
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
                list = ast.literal_eval(request.POST['id'])
                data = {"type": request.POST["type"] ,"id": list[0]}
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
    if request.method == "GET":
        plantslist = Plant.objects.filter(active=True)
        return render(request, "farmer/plants.html", {"form": Dnewplant(), "data": plantslist})

    if request.content_type == "application/json":
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

        if payload.get("type") != "fetch":
            return JsonResponse({"error": "Unsupported request type."}, status=400)

        try:
            plant = Plant.objects.get(id=payload.get("data"))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Invalid plant ID."}, status=400)
        except Plant.DoesNotExist:
            return JsonResponse({"error": "Plant not found."}, status=404)

        return JsonResponse({"result": [plant.seeds, plant.medium_weight]}, status=201)

    if request.POST.get("type") == "filter":
        data = filter_data(Plant, request.POST)
        return render(request, "farmer/plants.html", {"form": Dnewplant(), "data": data})

    uitem = updateitem(request.POST, Plant, Dnewplant)
    if uitem == True:
        return HttpResponseRedirect("plants")
    if uitem == False:
        return render(request, "farmer/plants.html", {"error": "SOMETHING WENT WRONG"})
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


def render_bulk_harvest_error(request, form):
    return render(request, "farmer/index.html", {
        "data": groupingtrays(),
        "form": Dnewtray(),
        "todayu": str(datetime.date(datetime.today())),
        "bulkharvest": form,
        "bulk_tray_ids": request.POST.get("id", ""),
    }, status=400)


@login_required
def harvest(request):
    if request.method == "POST":
        if request.POST.get("type") == "bulknew":
            try:
                create_bulk_harvest(request.POST.copy())
            except BulkHarvestValidationError as error:
                return render_bulk_harvest_error(request, error.form)
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
    allbulk = BulkHarvest.objects.all()[:10]
    report_filter = None
    form = Reportfilter()
    status = 200

    if request.method == "POST":
        if request.POST.get("type") == "delete":
            deleted = updateitem(request.POST, BulkHarvest, Nbulkharvest)
            if deleted:
                return HttpResponseRedirect(reverse("report"))
            return render(request, "farmer/report.html", {"error": "SOMETHING WENT WRONG"}, status=400)

        form = Reportfilter(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data["type"]
            product = form.cleaned_data["product"]
            start = form.cleaned_data["start"]
            end = form.cleaned_data["end"]
            report_filter = {"type": report_type, "product": product, "start": start, "end": end}

            allbulk = BulkHarvest.objects.filter(Harvestdate__range=[start, end])
            if product:
                allbulk = allbulk.filter(Product=product)

            if report_type == "Mix":
                totals = allbulk.aggregate(
                    medium=models.Sum("MediumWeightMix"),
                    totalyield=models.Sum("MixWeight"),
                )
                medium = totals["medium"] or 0
                totalyield = totals["totalyield"] or 0
        else:
            allbulk = BulkHarvest.objects.none()
            status = 400

    data = [row.serialize() for row in allbulk]
    return render(request, "farmer/report.html", {
        "data": data,
        "fform": form,
        "filter": report_filter,
        "medium": medium,
        "totalyield": totalyield,
        "rff": form,
    }, status=status)


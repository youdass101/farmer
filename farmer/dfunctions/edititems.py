from ..models import *
from ..forms import *
from django.contrib.postgres.aggregates import ArrayAgg


def trayser(type, sdata="all"):
    if sdata=="all":
        sdata = Tray.objects.all()
    # GET TODAYS DATE 
    cd = str(datetime.date(datetime.today()))

    data = [row.serialize() for row in sdata] 
    if type == "active":
        # GET ONLY ACTIVE NONE HARVEST TRAYS
        active = [x for x in data if not x["harvest"]]
    else:
        active = [x for x in data if x["harvest"]]
    
    return {"cd": cd, "active": active}


# update update tray
def updateitem (data, dobject, dform, att=1):
    type = data["type"] # type of action
    if type != "new":
        item = dobject.objects.get(id=data["id"]) # Tray object

    if type == "loadedit": # load edit form
        try:
            initial = {'count':att} # trays qtt
            form = dform(instance=item, count=att, initial = initial) # form with instance and count
        except:
            form = dform(instance=item) # form with instance if failed

        list = dobject.objects.all() # all trays 
        return {"editform": form, "form": dform(), "data": list}
    
    if type == "delete": # delete tray
        item.delete()
        return True

    if type == "edit": # edit tray
        nitem = dform(data, instance=item)

    if type == "new": # create new tray
        nitem = dform(data)

    if nitem.is_valid(): # check if form is valid
        nitem.save()
        return True

    else:
        return False



def check_number(count, cobject, item):
    try: 
        cobject.objects.get(number=count, name=item)
        count += 1
        count = check_number(count, cobject, item)
    except:
        if count == 0:
            count = 1
        else:
            return count
                
    return count

def collectanalyticdata(object):
    today = datetime.today()
    return {
        'name': Plant.objects.get(id=object['name']).name, 
        'start': datetime.date(object['start']), 
        'quantity': object['qtt'], 
        'end':datetime.date(object['start']) + timedelta(Plant.objects.get(id=object['name']).harvest),
        'days':datetime.date(today) - datetime.date(object['start']),
        'seeds': object['seeds'], 
        'soil': object['soil'],
        'listid': object['list_id'],
        'today': str(datetime.date(datetime.today()))
    }

def newobject(data, object, form ):
    try: 
        # GET COUNT OF TRAY BASED ON PLANT NAME 
        c = object.objects.filter(name=data['name']).count() 
    except:
        # IF THIS IS THE FRIST TRAY OF IT KIND 
        c = 0
    # CREATE NEW TRAY NUMBER
    for i in range(int(data['count'])):
        # TRAY NUMBER BY NAME
        c =check_number(c, Tray, data['name'])
        # ADD NUMBER TO NAME 
        data.update({'number':c})
        item = updateitem(data, object, form)
    return item

def groupingtrays ():
    try:
        # filter only non harvested trays
        active = Tray.objects.exclude(id__in= Harvest.objects.values('tray'))
        # group trays my name and date
        grouped = active.values('name', 'start').annotate(qtt=models.Count('name'), seeds=models.Sum('seeds_weight'), 
                                                        soil=models.Sum('medium_weight'), list_id=ArrayAgg('id'))
        # create empty list to add data
        data= [collectanalyticdata(row) for row in grouped.order_by('-start')]
    except:
        data = False


    return data

def filter_data(ob, data):
    if data["search"] != "":
        if ob == Tray:
            sdata = ob.objects.filter(fname__contains=data["search"])
        else:
            sdata = ob.objects.filter(name__contains=data["search"])
    else:
        sdata = ob.objects.all().order_by(data["filter"])   
    return sdata 

def filter_tray(ob, data, state):
    try:
        fdata = trayser(state, filter_data(ob, data))
    except:
        filter = data['filter']
        sdata = Tray.objects.all()
        vdata = [row.serialize() for row in sdata]
        fdata = sorted(vdata, key=lambda k: k[filter])

        if state == "active":
            active = [x for x in fdata if not x["harvest"]]
        else:
            active = [x for x in fdata if x["harvest"]]


        fdata = {"cd":str(datetime.date(datetime.today())), "active": active}

    return fdata




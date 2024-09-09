from ..models import *
from ..forms import *
from django.contrib.postgres.aggregates import ArrayAgg


def trayser(type):
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



def updateitem (data, dobject, dform, att=1):

    type = data["type"]
    if type == "loadedit":
        idi = data["itemid"]
        item = dobject.objects.get(id=idi)
        try:
            initial = {'count':att}
            form = dform(instance=item, count=att, initial = initial)

        except:
            form = dform(instance=item)

        list = dobject.objects.all()

        return {"editform": form, "form": dform(), "data": list}
    
    if type == "delete":
        print("first step")
        item = dobject.objects.get(id=data['id'])
        print("detele now")
        item.delete()
        return True

    if type == "edit":
        item = dobject.objects.get(id=data['id'])
        nitem = dform(data, instance=item)

    if type == "new":
        nitem = dform(data)

    if nitem.is_valid():
        nitem.save()

        return True

    else:
        print(nitem.errors)
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
        data= [collectanalyticdata(row) for row in grouped]
    except:
        data = False


    return data
 
    


    
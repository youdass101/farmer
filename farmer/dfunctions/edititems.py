from ..models import *
from ..forms import *

def trayser(type):
    sdata = Tray.objects.all()
    # GET TODAYS DATE 
    cd = str(datetime.date(datetime.today()))

    data = [row.serialize() for row in sdata] 
    if type == "active":
        # SERIALIZE EACH ROW WITH DETAILED DATA 
        data = [row.serialize() for row in sdata] 
        # GET ONLY ACTIVE NONE HARVEST TRAYS
        active = [x for x in data if not x["harvest"]]
    
        return {"cd": cd, "active": active}



def updateitem (data, dobject, dform):

    type = data["type"]
    if type == "loadedit":
        idi = data["itemid"]
        item = dobject.objects.get(id=idi)
        form = dform(instance=item)
        form.id = idi
        list = dobject.objects.all()

        return {"editform": form, "form": Dnewmedium(), "data": list}
    
    if type == "delete":
        item = dobject.objects.get(id=data['poid'])
        item.delete()
        list = dobject.objects.all()
        return True

    if type == "edit":
        item = dobject.objects.get(id=data['poid'])
        nitem = dform(data, instance=item)

    if type == "new":
        nitem = dform(data)

    if nitem.is_valid():
        nitem.save()
    else:
        return False
    
    list = dobject.objects.all()


    return True


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
    


    
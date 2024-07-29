from ..models import *
from ..forms import *



def Tray_edit(form):

    tray = Tray.objects.get(id=form['id'])

    if form['delete']:
        tray = Tray.objects.get(id=form['id'])
        tray.delete()
        # RETURN STATUS AND MSG 
    else:
        # EDIT TRAY FROM JS DATA IF DELET IS FLASE 
        medium = Medium.objects.get(name=form["medium"])
        tray = Tray.objects.get(id=form['id'])
        tray.medium = medium
        tray.medium_weight = form['medium_weight']
        tray.seeds_weight = form['seed']
        tray.start = datetime.strptime(form['start'], '%B %d, %Y')
        tray.save()

    return True

def Clean_data(form):

    if form.is_valid():
        for key in form.cleaned_data.items():
            print(key[0], key[1]) 
            exec(key[0] + '=key[1]')


def createnewtrays (form):
  
    # CHECK VALIDITY AND CLEAN FORM DATA
    Clean_data(form)
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
        
        return True

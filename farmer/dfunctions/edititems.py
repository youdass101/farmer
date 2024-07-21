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

    print(plant)
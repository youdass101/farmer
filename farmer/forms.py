from django import forms
from .models import *
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Dnewplant (forms.ModelForm):
    id = forms.IntegerField(required=False)
    id.widget = id.hidden_widget()
    class Meta:
        model = Plant
        fields = "__all__"
 


class Dnewmedium (forms.ModelForm):
    id = forms.IntegerField(required=False)
    id.widget = id.hidden_widget()
    class Meta:
        model = Medium
        fields = ["name", "soil", "coco", "id"]

class Nharvest (forms.ModelForm):
    id = forms.IntegerField(required=False)
    id.widget = id.hidden_widget()
    class Meta:
        model = Harvest
        fields = ["tray", "date", "output", "id"]
        widgets = {
        'date': forms.SelectDateWidget(attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
        'tray': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(Nharvest, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.now()


class Dnewtray(forms.ModelForm):
    id = forms.IntegerField(required=False)
    id.widget = id.hidden_widget()
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'How many tray', 'value':'1'}),label=('QTT'))
    class Meta:
        model = Tray
        fields = ["name", "medium", "seeds_weight", "medium_weight", "start", "number", "count", "id"]
        widgets = {
        'start': forms.SelectDateWidget(attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
        'number': forms.HiddenInput(),
    }
        # labels = {
        #     "name": _("Plant"),
        # }

    
    def __init__(self, *args, count=1, **kwargs):
        super(Dnewtray, self).__init__(*args, **kwargs)
        self.fields['start'].initial = datetime.now()
        self.fields['medium'].initial = ['1']

        self.fields['count'].widget.attrs['max'] = count
        self.fields['count'].widget.attrs['min'] = 1



class Nbulkharvest(forms.ModelForm):
    class Meta:
        model = BulkHarvest
        fields = ["Trays","PacksQtt", "MixWeight", "Harvestdate"]


class Reportfilter(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class':'toset'}),label=('select type'),choices=(("All","All"),("Packs","Packs"),("Mix","Mix")))
    product = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='All',required=False, queryset=Plant.objects.all())
    start = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'toset'}),label=('Starting'),initial=datetime.now())
    end = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'toset'}),label=('Ending'),initial=datetime.now())

class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))

class Register(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'inputs', 'placeholder':'Email'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Comfirm password'}),label=(''))
    regcode = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Registration Code'}),label=(''))


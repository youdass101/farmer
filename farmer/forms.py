from django import forms
from .models import *
from datetime import datetime


class Newplant(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'toset', 'placeholder':'Plant Name'}),label=(''))
    seeds = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'seeds weight'}),label=(''))
    pressure = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'days of Presssure'}),label=(''))
    blackout = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'days of blackout'}),label=(''))
    harvest = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'time to harvest'}),label=(''))
    output = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'Harvest output'}),label=(''))

class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))

class Register(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'inputs', 'placeholder':'Email'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Comfirm password'}),label=(''))
    regcode = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Registration Code'}),label=(''))

class Newmedium(forms.Form):
    name =  forms.CharField(widget=forms.TextInput(attrs={'class':'toset', 'placeholder':'Medium name'}),label=(''))
    soil = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'Soil percentage'}),label=(''))
    coco = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'coco percentage'}),label=(''))


class Newtray(forms.Form):
    plant = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Plant',label=(''),queryset=Plant.objects.all())
    medium = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Medium',label=(''),queryset=Medium.objects.all())
    seed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset'}),label=(''), required=False)
    medium_weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset',"value":"130", 'placeholder':'Medium Weight'}),label=(''))
    start = forms.DateField(widget=forms.SelectDateWidget(attrs={'class':'toset'}),label=(''),initial=datetime.today())
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'How many tray', 'value':'1'}),label=(''))

class Edittray(forms.Form):
    medium = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Medium',label=(''),queryset=Medium.objects.all())
    seed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset'}),label=(''), required=False)
    medium_weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset',"value":"130", 'placeholder':'Medium Weight'}),label=(''))
    start = forms.DateField(initial=datetime.today())

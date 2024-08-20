from django import forms
from .models import *
from datetime import datetime

class Dnewplant (forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "seeds", "pressure", "blackout", "harvest", "medium_weight", "packweight"]


class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))

class Register(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Username'}),label=(''))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'inputs', 'placeholder':'Email'}),label=(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Password'}),label=(''))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs', 'placeholder':'Comfirm password'}),label=(''))
    regcode = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs', 'placeholder':'Registration Code'}),label=(''))


class Dnewmedium (forms.ModelForm):
    class Meta:
        model = Medium
        fields = ["name", "soil", "coco"]


class Newtray(forms.Form):
    plant = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Plant',label=(''),queryset=Plant.objects.all())
    medium = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Medium',label=(''),queryset=Medium.objects.all(), initial= ['2'])
    seed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset'}),label=(''), required=False)
    medium_weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'Medium Weight'}),label=(''))
    start = forms.DateField(widget=forms.SelectDateWidget(attrs={'class':'toset'}),label=(''),initial=datetime.now())
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset', 'placeholder':'How many tray', 'value':'1'}),label=(''))
    location = forms.ChoiceField(widget=forms.Select(attrs={'class':'toset'}),label=('Location'),choices=(("H","H"),("D","D")))

class Dnewtray(forms.ModelForm):
    count = forms.IntegerField()
    class Meta:
        model = Tray
        fields = ["name", "medium", "seeds_weight", "medium_weight", "start"]
        widgets = {
        'start': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start'].initial = datetime.now()


class Edittray(forms.Form):
    medium = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='Select the Medium',queryset=Medium.objects.all())
    seed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset'}), required=False)
    medium_weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'toset',"value":"130", 'placeholder':'Medium Weight'}))
    start = forms.DateField(initial=datetime.today())

class Reportfilter(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class':'toset'}),label=('select type'),choices=(("All","All"),("Packs","Packs"),("Mix","Mix")))
    product = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='All',required=False, queryset=Plant.objects.all())
    start = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'toset'}),label=('Starting'),initial=datetime.now())
    end = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'toset'}),label=('Ending'),initial=datetime.now())


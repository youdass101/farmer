from django import forms

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


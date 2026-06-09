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
        fields = ["tray", "date", "output", "id", "bulkh"]
        widgets = {
        'date': forms.SelectDateWidget(years=range(2023, 2030), attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
        'tray': forms.HiddenInput(),
        'bulkh': forms.HiddenInput(),

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
        'start': forms.SelectDateWidget(years=range(2023, 2030), attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
        'number': forms.HiddenInput(),
        }

    
    def __init__(self, *args, count=None, **kwargs):
        super(Dnewtray, self).__init__(*args, **kwargs)
        self.fields['start'].initial = datetime.now()
        self.fields['medium'].initial = ['1']
        self.fields['name'].queryset = Plant.objects.filter(active=True)  # Only active mediums
        self.fields['medium'].queryset = Medium.objects.all()  # Show all Mediums
        self.fields['medium'].initial = Medium.objects.first()  # Default to first Medium        self.fields['count'].widget.attrs['max'] = count
        self.fields['count'].widget.attrs['min'] = 1



class Nbulkharvest(forms.ModelForm):
    class Meta:
        model = BulkHarvest
        fields = ["Product", "MediumMix", "Trays", "PacksQtt", "MixWeight", "Harvestdate"]

        widgets = {
            'Harvestdate': forms.SelectDateWidget(years=range(2023, 2030),attrs={'class':'toset', 'placeholder':'Select a date', 'type':'date'}),
            'Product': forms.HiddenInput(),
            'MediumMix': forms.HiddenInput(),
            }
    
    def __init__(self, *args, **kwargs):
        super(Nbulkharvest, self).__init__(*args, **kwargs)
        self.fields['Harvestdate'].initial = datetime.now()
        self.fields['Trays'].widget.attrs['min'] = 1

    def clean(self):
        cleaned_data = super().clean()
        trays = cleaned_data.get("Trays")
        packs_quantity = cleaned_data.get("PacksQtt")
        mix_weight = cleaned_data.get("MixWeight")

        if trays is not None and trays < 1:
            self.add_error("Trays", "Select at least one tray.")
        if packs_quantity is not None and packs_quantity < 0:
            self.add_error("PacksQtt", "Pack quantity cannot be negative.")
        if mix_weight is not None and mix_weight < 0:
            self.add_error("MixWeight", "Mix weight cannot be negative.")
        if packs_quantity == 0 and mix_weight == 0:
            self.add_error(None, "Harvest output must be greater than zero.")

        return cleaned_data



class Reportfilter(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class':'toset'}),label=('select type'),choices=(("All","All"),("Packs","Packs"),("Mix","Mix")))
    product = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'toset'}), empty_label='All',required=False, queryset=Plant.objects.all())
    start = forms.DateField(widget=forms.SelectDateWidget(years=range(2023, 2030),attrs={'class': 'toset'}),label=('Starting'),initial=datetime.now())
    end = forms.DateField(widget=forms.SelectDateWidget(years=range(2023, 2030),attrs={'class': 'toset'}),label=('Ending'),initial=datetime.now())


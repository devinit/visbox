from django.contrib import admin
from core.models import Dataset, Visualisation
from django import forms
from core.forms import *
from django.forms import ModelForm

class UploadAdminForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name','data','sep']
        SEP_CHOICES = [
            ("\t","Tab (pasted from Excel)"),
            (",","Comma"),
            ("|","Pipe"),
        ]
        widgets = {
            'sep':forms.RadioSelect(choices=SEP_CHOICES)
        }
    def __init__(self, *args, **kwargs):
        super(UploadAdminForm, self).__init__(*args, **kwargs)
        self.fields['sep'].strip = False

# Register your models here.
class DatasetAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['name','creator','created','sep']
    #enable the save buttons on top of change form
    save_on_top = True
    #Pull in custom form
    form = UploadAdminForm
    
class VisualisationAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['title','dataset','creator','created']
    #enable the save buttons on top of change form
    save_on_top = True

    
admin.site.register(Dataset,DatasetAdmin)
admin.site.register(Visualisation,VisualisationAdmin)

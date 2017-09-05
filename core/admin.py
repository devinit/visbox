from django.contrib import admin
from core.models import Dataset, Visualisation
from django import forms
from core.forms import *
from django.forms import ModelForm
from glob import glob
from django.conf import settings
from os.path import basename

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
def pull_ddw(modeladmin,request,queryset):
    ddw_datasets = glob(settings.STATIC_ROOT+'/core/data/*.csv')
    for ddw_dataset in ddw_datasets:
        dataset = Dataset()
        dataset.name = basename(ddw_dataset)
        dataset.data = open(ddw_dataset)
        dataset.creator = User.objects.get(username=request.user)
        dataset.sep=","
        dataset.save()

class DatasetAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['name','creator','created','sep']
    #enable the save buttons on top of change form
    save_on_top = True
    #Pull in custom form
    form = UploadAdminForm
    actions = [pull_ddw]
    
class VisualisationAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['title','dataset','creator','created']
    #enable the save buttons on top of change form
    save_on_top = True

    
admin.site.register(Dataset,DatasetAdmin)
admin.site.register(Visualisation,VisualisationAdmin)

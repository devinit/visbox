from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import *
from django.contrib.auth import authenticate, login, logout
from core.forms import *
from core.models import Dataset, Visualisation
from django.contrib.auth.models import User
import pandas as pd
from StringIO import StringIO
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from django.core.urlresolvers import reverse
from utils import *
from django.core.files.temp import NamedTemporaryFile
import decimal
from django.conf import settings

def index(request):
    user = request.user
    return render_to_response('core/home.html', {"user":user})

def signup(request):
    logout(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return render_to_response('core/home.html', {"user":user})
    else:
        form = SignUpForm()
    return render(request,'core/signup.html',{'form':form})

@login_required
def start(request):
    user = request.user
    staff = User.objects.filter(is_staff=True)
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            dataset = form.save(commit=False)
            if dataset.sep == "t":
                dataset.sep = "\t"
            dataset.creator = User.objects.get(username=user)
            dataset.save()
            form = UploadForm()
    else:
        form = UploadForm()
    datasets = Dataset.objects.filter(creator=user)
    staff_datasets = Dataset.objects.filter(creator__in=staff)
    return render(request,'core/start.html', {"user":user,"datasets":datasets,"staff_datasets":staff_datasets,"form":form})

@login_required
def gallery(request):
    user = request.user
    visualisations = Visualisation.objects.all()
    return render_to_response('core/gallery.html', {"user":user,"visualisations":visualisations})

@login_required
def dataset(request,datasetPK):
    user = request.user
    staff = User.objects.filter(is_staff=True)
    templates = Visualisation.objects.filter(save_as_template=True,creator__in=staff)
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.header = list(dataset.df)
    dataset.types = [(header, dataset.df.dtypes[header]) for header in dataset.header]
    dataset.table = dataset.df.to_html()
    
    schema_file = open(settings.STATIC_ROOT+'/core/js/di-charts.schema.json')   
    schemas = json.load(schema_file)         
    schema_file.close()
    chart_types = [schema["name"] for schema in schemas]
    
    return render_to_response('core/dataset.html', {"user":user,"dataset":dataset,"templates":templates,"chart_types":chart_types})

@login_required
def deleteDataset(request,datasetPK):
    if request.method == 'POST':
        user = request.user
        dataset = get_object_or_404(Dataset,pk=datasetPK)
        if dataset.creator == user:
            dataset.delete()
            return HttpResponse('OK')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()
    
@login_required
def createVis(request,chart,datasetPK):
    user = request.user
    
    schema_file = open(settings.STATIC_ROOT+'/core/js/di-charts.schema.json')   
    schemas = json.load(schema_file)         
    schema_file.close()
    
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.variables = list(dataset.df)
    
    filtered_schema = [schema for schema in schemas if schema['name'] == chart]
    if len(filtered_schema)>0:
        chartSchema = filtered_schema[0]
        if request.method=="POST":
            form = VisForm(request.POST,schema=chartSchema,variables=dataset.variables)
            if form.is_valid():
                config = form.cleaned_data
                visualisation = Visualisation()
                visualisation.title = config['config.title']
                visualisation.chart_type = chart
                visualisation.dataset = dataset
                visualisation.creator = User.objects.get(username=user)
                visualisation.save_as_template = config['save_as_template']
                visualisation.configuration_flat = config
                visualisation.configuration = nest_config(config)
                visualisation.save()
                return redirect('core.views.viewVis',chartPK=visualisation.pk)
            else:
                #Vis invalid
                return render(request,'core/chart/create.html', {"user":user,"dataset":dataset,"form":form,"chart":chart})
        else:
            #GET request
            chartPK = request.GET.get("copy",False)
            if chartPK:
                visualisation = Visualisation.objects.get(pk=chartPK)
                form = VisForm(instance=visualisation,schema=chartSchema,variables=dataset.variables)
            else:
                visualisation = None
                form = VisForm(schema=chartSchema,variables=dataset.variables)
            return render(request,'core/chart/create.html', {"user":user,"dataset":dataset,"form":form,"chart":chart,"visualisation":visualisation})
    else:
        return render_to_response('core/construction.html', {"user":user})
    
@login_required
def viewVis(request,chartPK):
    user = request.user
    
    schema_file = open(settings.STATIC_ROOT+'/core/js/di-charts.schema.json')   
    schemas = json.load(schema_file)         
    schema_file.close()
    
    visualisation = get_object_or_404(Visualisation,pk=chartPK)
    
    filtered_schema = [schema for schema in schemas if schema['name'] == visualisation.chart_type]
    
    dataset = get_object_or_404(Dataset,pk=visualisation.dataset.pk)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.variables = list(dataset.df)
    if len(filtered_schema)>0:
        chartSchema = filtered_schema[0]
        form = VisForm(instance=visualisation,schema=chartSchema,variables=dataset.variables)
        return render(request,'core/chart/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    else:
        return HttpResponse("This is where you would view chart with primary key: "+str(chartPK))

@login_required
def editVis(request,chartPK):
    user = request.user
    
    schema_file = open(settings.STATIC_ROOT+'/core/js/di-charts.schema.json')   
    schemas = json.load(schema_file)         
    schema_file.close()
    
    visualisation = get_object_or_404(Visualisation,pk=chartPK)
    
    filtered_schema = [schema for schema in schemas if schema['name'] == visualisation.chart_type]
    
    dataset = get_object_or_404(Dataset,pk=visualisation.dataset.pk)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.variables = list(dataset.df)
    
    if len(filtered_schema)>0:
        chartSchema = filtered_schema[0]
        form = VisForm(request.POST or None, instance=visualisation,schema=chartSchema,variables=dataset.variables)
        if form.is_valid():
            config = form.cleaned_data
            visualisation.title = config['config.title']
            visualisation.save_as_template = config['save_as_template']
            visualisation.configuration_flat = config
            visualisation.configuration = nest_config(config)
            visualisation.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/chart/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    return HttpResponse("This is where you would edit chart with primary key: "+str(chartPK))

@login_required
def deleteVis(request,chartPK):
    user = request.user
    visualisation = get_object_or_404(Visualisation,pk=chartPK)
    if user == visualisation.creator:
        visualisation.delete()
        return redirect('core.views.gallery')
    else:
        return HttpResponseForbidden()

def csv(request,datasetPK):
    user = request.user
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    response = HttpResponse(df.to_csv(index=False))
    response['Filename'] = str(datasetPK)+".csv"
    response['Content-Disposition'] = 'attachment; filename='+str(datasetPK)+".csv"
    return response

def api(request,templatePK):
    if request.method=="GET":
        
        schema_file = open(settings.STATIC_ROOT+'/core/js/di-charts.schema.json')   
        schemas = json.load(schema_file)         
        schema_file.close()
        
        visualisation = get_object_or_404(Visualisation,pk=templatePK)
        
        filtered_schema = [schema for schema in schemas if schema['name'] == visualisation.chart_type]
        
        dataString = request.GET.get("data",False)
        filterSelection = request.GET.get("filter",False)
        if dataString:
            dataset = None
            df = pd.read_json(dataString)
            variables = list(df)
        else:
            dataset = visualisation.dataset
            df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
            variables = list(df)
        if len(filtered_schema)>0:
            chartSchema = filtered_schema[0]
            form = VisForm(instance=visualisation,schema=chartSchema,variables=variables)
            return render(request,'core/chart/api.html',{"form":form,"dataset":dataset,"filter":filterSelection,"visualisation":visualisation,"dataString":dataString})
        else:
            response = HttpResponse("Sorry, invalid chart type.")
            return response
    else:
        response = HttpResponse("Please only GET to this URL.")
        return response

def config(request,templatePK):
    if request.method=="GET":
        visualisation = get_object_or_404(Visualisation,pk=templatePK)
        config = visualisation.configuration
        return HttpResponse(json.dumps(config), content_type="application/json")
    else:
        response = HttpResponse("Please only GET to this URL.")
        return response
    
def png(request,templatePK):
    visualisation = get_object_or_404(Visualisation,pk=templatePK)
    dataString = request.GET.get("data",False)
    filterSelection = request.GET.get("filter",False)
    base_url = "http://127.0.0.1"+reverse('core.views.api',kwargs={"templatePK":templatePK})
    url = base_url
    if dataString:
        url = base_url+"?data="+dataString
    if filterSelection:
        url = base_url+"?filter="+filterSelection
    if dataString and filterSelection:
        url = base_url+"?data="+dataString+"&filter="+filterSelection
        

    newPNG = NamedTemporaryFile(suffix='.png')
    chromePNG(url,newPNG.name)
    response = HttpResponse(newPNG,content_type="image/png")
    response['Filename'] = visualisation.title+".png"
    response['Content-Disposition'] = 'attachment; filename='+visualisation.title+".png"
    return response

def svg(request,templatePK):
    visualisation = get_object_or_404(Visualisation,pk=templatePK)
    dataString = request.GET.get("data",False)
    filterSelection = request.GET.get("filter",False)
    base_url = "http://127.0.0.1"+reverse('core.views.api',kwargs={"templatePK":templatePK})
    url = base_url
    if dataString:
        url = base_url+"?data="+dataString
    if filterSelection:
        url = base_url+"?filter="+filterSelection
    if dataString and filterSelection:
        url = base_url+"?data="+dataString+"&filter="+filterSelection

    source_code = chromeSVG(url)
    response = HttpResponse(source_code,content_type="image/svg+xml")
    response['Filename'] = visualisation.title+".svg"
    response['Content-Disposition'] = 'attachment; filename='+visualisation.title+".svg"
    return response


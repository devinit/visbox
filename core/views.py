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
    return render_to_response('core/dataset.html', {"user":user,"dataset":dataset,"templates":templates})

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
    
    schema_file = open(settings.STATIC_ROOT+'/core/js/charts/test_schema.json')   
    schemas = json.load(schema_file)         
    schema_file.close()
    
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.variables = list(dataset.df)
    if chart in schemas:
        if request.method=="POST":
            form = VisForm(request.POST,schema=schemas[chart],variables=dataset.variables)
            if form.is_valid():
                visualisation = form.save(commit=False)
                visualisation.creator = User.objects.get(username=user)
                visualisation.dataset = dataset
                visualisation.save()
                return redirect('core.views.viewVis',chartPK=visualisation.pk)
            else:
                #Vis invalid
                return render(request,'core/column/create.html', {"user":user,"dataset":dataset,"form":form})
        else:
            #GET request
            chartPK = request.GET.get("copy",False)
            if chartPK:
                form = VisForm(instance=Visualisation.objects.get(pk=chartPK),schema=schemas[chart],variables=dataset.variables)
            else:
                form = VisForm(schema=schemas[chart],variables=dataset.variables)
            return render(request,'core/chart/create.html', {"user":user,"dataset":dataset,"form":form,"copy":chartPK})
    else:
        return render_to_response('core/construction.html', {"user":user})
    
@login_required
def viewVis(request,chartPK):
    user = request.user
    visualisation = get_object_or_404(Visualisation,pk=chartPK)
    dataset = get_object_or_404(Dataset,pk=visualisation.dataset.pk)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.categorical = list(dataset.df.select_dtypes(include=['object']))
    dataset.numerical = list(dataset.df.select_dtypes(exclude=['object']))
    if visualisation.chart_type == "column":
        form = ColumnForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/column/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "bar":
        form = BarForm(instance=visualisation,x=dataset.numerical,y=dataset.categorical)
        return render(request,'core/bar/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "stacked_column":
        form = StackedColumnForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/stacked_column/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "donut":
        form = DonutForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/donut/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "pie":
        form = DonutForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/pie/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "line":
        form = LineForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/line/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "grouped_column":
        form = StackedColumnForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/grouped_column/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "bubble":
        form = BubbleForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/bubble/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "area":
        form = StackedColumnForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/area/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "tree":
        form = TreeForm(instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        return render(request,'core/tree/view.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    return HttpResponse("This is where you would view chart with primary key: "+str(chartPK))

@login_required
def editVis(request,chartPK):
    user = request.user
    visualisation = get_object_or_404(Visualisation,pk=chartPK)
    dataset = get_object_or_404(Dataset,pk=visualisation.dataset.pk)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.categorical = list(dataset.df.select_dtypes(include=['object']))
    dataset.numerical = list(dataset.df.select_dtypes(exclude=['object']))
    if visualisation.chart_type == "column":
        form = ColumnForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/column/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "bar":
        form = BarForm(request.POST or None, instance=visualisation,x=dataset.numerical,y=dataset.categorical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/bar/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "stacked_column":
        form = StackedColumnForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/stacked_column/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "donut":
        form = DonutForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/donut/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "pie":
        form = DonutForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/pie/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "line":
        form = LineForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/line/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "grouped_column":
        form = StackedColumnForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/grouped_column/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "bubble":
        form = BubbleForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/bubble/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "area":
        form = StackedColumnForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/area/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
    if visualisation.chart_type == "tree":
        form = TreeForm(request.POST or None, instance=visualisation,x=dataset.categorical,y=dataset.numerical)
        if form.is_valid():
            form.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        return render(request,'core/tree/edit.html',{"user":user,"form":form,"dataset":dataset,"visualisation":visualisation})
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
        visualisation = get_object_or_404(Visualisation,pk=templatePK)
        chart_type = visualisation.chart_type
        
        dataString = request.GET.get("data",False)
        filterSelection = request.GET.get("filter",False)
        if dataString:
            dataset = None
            df = pd.read_json(dataString)
            categorical = list(df.select_dtypes(include=['object']))
            numerical = list(df.select_dtypes(exclude=['object']))
        else:
            dataset = visualisation.dataset
            df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
            categorical = list(df.select_dtypes(include=['object']))
            numerical = list(df.select_dtypes(exclude=['object']))
        if chart_type == "column":
            form = ColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "bar":
            form = BarForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "donut":
            form = DonutForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "pie":
            form = DonutForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "stacked_column":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "line":
            form = LineForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "grouped_column":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "bubble":
            form = BubbleForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "area":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "tree":
            form = TreeForm(instance=visualisation,x=categorical,y=numerical)
        return render(request,'core/'+chart_type+'/api.html',{"form":form,"dataset":dataset,"filter":filterSelection,"visualisation":visualisation,"dataString":dataString})
    else:
        response = HttpResponse("Please only GET to this URL.")
        return response
    
def config(request,templatePK):
    if request.method=="GET":
        fileFormat = request.GET.get("format",False)
        
        config = {}
        root = Element("config")
               
        visualisation = get_object_or_404(Visualisation,pk=templatePK)
        chart_type = visualisation.chart_type

        dataset = visualisation.dataset
        df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
        categorical = list(df.select_dtypes(include=['object']))
        numerical = list(df.select_dtypes(exclude=['object']))
        if chart_type == "column":
            form = ColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "bar":
            form = BarForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "donut":
            form = DonutForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "pie":
            form = DonutForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "stacked_column":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "grouped_column":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "line":
            form = LineForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "bubble":
            form = BubbleForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "area":
            form = StackedColumnForm(instance=visualisation,x=categorical,y=numerical)
        if chart_type == "tree":
            form = TreeForm(instance=visualisation,x=categorical,y=numerical)
        config['template'] = int(templatePK)
        child = SubElement(root,"template")
        child.text = str(templatePK)
        for field in form:
            val = field.value()
            if isinstance(val,decimal.Decimal):
                val = float(val)
            config[field.html_name] = val
            child = SubElement(root,field.html_name)
            child.text = str(field.value())
        
        if fileFormat=="json":
            return HttpResponse(json.dumps(config), content_type="application/json")
        if fileFormat=="xml":
            return HttpResponse(tostring(root, encoding='utf8', method='xml'),content_type='text/xml')
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


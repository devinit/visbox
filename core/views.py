from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import *
from django.contrib.auth import authenticate, login, logout
from core.forms import SignUpForm, UploadForm, VisForm
from core.models import Dataset, Visualisation
from django.contrib.auth.models import User
import pandas as pd
from StringIO import StringIO
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages


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
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.creator = User.objects.get(username=user)
            dataset.sep = "\t"
            dataset.save()
    form = UploadForm()
    datasets = Dataset.objects.filter(creator=user)
    for dataset in datasets:
        df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
        dataset.table = df.to_html()
    return render(request,'core/start.html', {"user":user,"datasets":datasets,"form":form})

@login_required
def gallery(request):
    user = request.user
    return render_to_response('core/gallery.html', {"user":user})

@login_required
def dataset(request,datasetPK):
    user = request.user
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.header = list(dataset.df)
    dataset.types = [(header, dataset.df.dtypes[header]) for header in dataset.header]
    dataset.table = dataset.df.to_html()
    return render_to_response('core/dataset.html', {"user":user,"dataset":dataset})

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
def create(request,chart,datasetPK):
    user = request.user
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    dataset.df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    dataset.categorical = list(dataset.df.select_dtypes(include=['object']))
    dataset.numerical = list(dataset.df.select_dtypes(exclude=['object']))
    if chart=="column":
        return render(request,'core/column.html', {"user":user,"dataset":dataset})
    return render_to_response('core/construction.html', {"user":user})

@login_required
def createVis(request):
    user = request.user
    if request.method=="POST":
        form = VisForm(request.POST)
        if form.is_valid():
            visualisation = form.save(commit=False)
            visualisation.creator = User.objects.get(username=user)
            visualisation.dataset = Dataset.objects.get(pk=request.POST.get("datasetPK"))
            visualisation.save()
            return redirect('core.views.viewVis',chartPK=visualisation.pk)
        else:
            #Vis invalid
            return HttpResponse("Sorry, something went wrong.")
    else:
        return HttpResponse("Sorry, something went wrong.")
    
@login_required
def viewVis(request,chartPK):
    return HttpResponse(chartPK)

def csv(request,datasetPK):
    user = request.user
    dataset = get_object_or_404(Dataset,pk=datasetPK)
    df = pd.read_csv(StringIO(dataset.data),sep=dataset.sep)
    response = HttpResponse(df.to_csv(index=False))
    response['Filename'] = str(datasetPK)+".csv"
    response['Content-Disposition'] = 'attachment; filename='+str(datasetPK)+".csv"
    return response
        


from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'covidMap/Map1.html')

def data(request):
    return render(request, 'covidMap/data.html')

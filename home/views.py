from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'Covid_Map/Map1.html')

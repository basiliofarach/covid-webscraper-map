from django.shortcuts import render

# Create your views here.
def graphs(request):
    return render(request, 'dataGraphs/Population.html')

def total_cases(request):
    return render(request, 'dataGraphs/TotalCases.html')

def mortality(request):
    return render(request, 'dataGraphs/Mortality.html')

def mortality_closed(request):
    return render(request, 'dataGraphs/MortalityClosed.html')

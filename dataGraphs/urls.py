from django.urls import path
from . import views

urlpatterns = [
    path('graph', views.graphs, name= 'graph'),
    path('total_cases', views.total_cases, name= 'total_cases'),
    path('mortality', views.mortality, name= 'mortality'),
    path('mortality_closed', views.mortality_closed, name= 'mortality_closed'),

]

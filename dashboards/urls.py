from django.urls import path
from .views import dash_graph

urlpatterns = [
    path('', dash_graph, name='dash-graph'),
]
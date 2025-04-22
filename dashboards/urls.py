from django.urls import path
from .views import *

urlpatterns = [
    path('y2y', dash_graph, name='y2y'),
    path('', plotly_dash, name='home'),
]
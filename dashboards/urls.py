from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView

urlpatterns = [
    path("y2y", dash_graph, name="y2y"),
    path("", login_view, name="login"),
    path("info", info, name="info"),
    path("dash", plotly_dash, name="home"),
    path("logout", logout_user, name="logout"),
    path("tenders", tenders, name="tenders"),
]

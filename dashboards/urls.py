from django.urls import path, include
from .views import *
from .views_api import *
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views_api import TenderContentViewSet

router = DefaultRouter()
router.register(r"tendercontent", TenderContentViewSet)
router.register(r"offers", OffersViewSet)
router.register(r"winners", WinnersViewSet)
router.register(r"actions", ActionsViewSet)

urlpatterns = [
    path("y2y", dash_graph, name="y2y"),
    path("", login_view, name="login"),
    path("info", info, name="info"),
    path("dash", plotly_dash, name="home"),
    path("logout", logout_user, name="logout"),
    path("tenders", tenders, name="tenders"),
    # API
    path("api/get_models/", get_models, name="get_models"),
    path("api/get_colors/<str:model>/", get_colors, name="get_colors"),
    path("api/full_table/", get_full_table, name="get_all"),
    path("api/", include(router.urls)),
]

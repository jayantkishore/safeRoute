from django.urls import path
from .views import HomePageView, AboutPageView, V1View, clusterView

urlpatterns = [
    path("route", V1View.as_view()),
    path("cluster", clusterView.as_view()),
    path("about", AboutPageView.as_view(), name="about"),
    path("", HomePageView.as_view(), name="home"),
]

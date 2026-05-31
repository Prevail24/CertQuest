from django.urls import path
from .views import dashboard, choose_path

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("choose-path/", choose_path, name="choose_path"),
]
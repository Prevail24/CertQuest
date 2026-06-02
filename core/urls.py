from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("users.urls")),
    path("", include("games.urls")),
    path("", include("quests.urls")),
    path("", include("learning.urls")),

]
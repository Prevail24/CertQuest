from django.urls import path
from .views import game_list

urlpatterns = [
    path("games/", game_list, name="game_list"),
]
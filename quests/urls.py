from django.urls import path
from .views import daily_quiz, scenario_detail, scenario_step, boss_battle_detail


urlpatterns = [
    
    path("games/scenario/<int:scenario_id>/", scenario_detail, name="scenario_detail"),
    path("games/daily-quiz/", daily_quiz, name="daily_quiz"),
    path("games/scenario/<int:scenario_id>/step/", scenario_step, name="scenario_step"),
    path("boss-battles/<int:boss_id>/", boss_battle_detail, name="boss_battle_detail"),
]
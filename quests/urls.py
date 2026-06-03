from django.urls import path
from .views import boss_battle_question, daily_quiz, scenario_detail, scenario_step, boss_battle_detail, boss_battle_start, boss_battle_question, boss_battle_complete


urlpatterns = [
    
    path("games/scenario/<int:scenario_id>/", scenario_detail, name="scenario_detail"),
    path("games/daily-quiz/", daily_quiz, name="daily_quiz"),
    path("games/scenario/<int:scenario_id>/step/", scenario_step, name="scenario_step"),
    path("boss-battles/<int:boss_id>/", boss_battle_detail, name="boss_battle_detail"),
    path("boss-battles/<int:boss_id>/start/", boss_battle_start,name="boss_battle_start"),
    path("boss-battles/<int:boss_id>/question/", boss_battle_question, name="boss_battle_question"),
    path("boss-battles/<int:boss_id>/complete/", boss_battle_complete, name="boss_battle_complete"),
]
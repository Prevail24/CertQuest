from django.urls import path
from .views import daily_quiz, scenario_detail, scenario_step


urlpatterns = [
    
    path("games/scenario/<int:scenario_id>/", scenario_detail, name="scenario_detail"),
    path("games/daily-quiz/", daily_quiz, name="daily_quiz"),
    path("games/scenario/<int:scenario_id>/step/", scenario_step, name="scenario_step")
    
]
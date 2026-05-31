from django.urls import path
from .views import daily_quiz

urlpatterns = [
    path(
        "games/daily-quiz/",
        daily_quiz,
        name="daily_quiz"
    ),
]
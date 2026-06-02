from django.urls import path
from .views import flashcard_study

urlpatterns = [
    path("flashcards/", flashcard_study, name="flashcard_study"),
]
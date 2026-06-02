from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from random import choice

from .models import Flashcard


@login_required
def flashcard_study(request):
    profile = request.user.profile

    if profile.selected_path:
        flashcards = list(
            Flashcard.objects.filter(
                certification_path=profile.selected_path,
                is_active=True
            )
        )
    else:
        flashcards = list(
            Flashcard.objects.filter(is_active=True)
        )

    if not flashcards:
        return render(request, "learning/no_flashcards.html")

    flashcard = choice(flashcards)

    return render(
        request,
        "learning/flashcard_study.html",
        {
            "flashcard": flashcard,
        }
    )
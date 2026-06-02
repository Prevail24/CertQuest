from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from random import choice
from django.db import models

from .models import Flashcard, UserFlashcard


@login_required
def flashcard_study(request):

    profile = request.user.profile

    if request.method == "POST":

        flashcard_id = request.POST.get("flashcard_id")
        action = request.POST.get("action")

        flashcard = Flashcard.objects.get(
            id=flashcard_id
        )

        user_flashcard, created = (
            UserFlashcard.objects.get_or_create(
                user=request.user,
                flashcard=flashcard
            )
        )

        user_flashcard.times_seen += 1

        if action == "correct":
            user_flashcard.times_correct += 1

        if action == "incorrect":
            user_flashcard.times_incorrect += 1

        user_flashcard.last_reviewed = timezone.now()
        user_flashcard.save()

        return redirect("flashcard_study")

    if profile.selected_path:

        flashcards = list(
            Flashcard.objects.filter(
                certification_path=profile.selected_path,
                is_active=True
            )
        )

    else:

        flashcards = list(
            Flashcard.objects.filter(
                is_active=True
            )
        )

    if not flashcards:

        return render(
            request,
            "learning/no_flashcards.html"
        )

    need_practice_ids = UserFlashcard.objects.filter(
        user=request.user,
        times_incorrect__gte=models.F("times_correct")
    ).values_list(
        "flashcard_id",
        flat=True
    )

    priority_cards = list(
        Flashcard.objects.filter(
            id__in=need_practice_ids,
            certification_path=profile.selected_path,
            is_active=True
        )
    )

    if priority_cards:
        flashcard = choice(priority_cards)
    else:
        flashcard = choice(flashcards)

    return render(
        request,
        "learning/flashcard_study.html",
        {
            "flashcard": flashcard,
        }
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models

from learning.models import CertificationPath, UserFlashcard
from achievements.models import UserAchievement
from learning.services import get_domain_progress


@login_required
def dashboard(request):
    """
    Displays the logged-in player's dashboard with:
    - level
    - XP progress
    - streak
    - unlocked achievements
    - domain progress
    - flashcard mastery
    """

    profile = request.user.profile

    xp_needed = profile.level * 100
    xp_percent = int((profile.xp / xp_needed) * 100)

    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related("achievement")

    domain_progress = get_domain_progress(request.user)

    user_flashcards = UserFlashcard.objects.filter(
        user=request.user
    )

    cards_reviewed = user_flashcards.count()

    known_cards = user_flashcards.filter(
        times_correct__gt=models.F("times_incorrect")
    ).count()

    practice_cards = user_flashcards.filter(
        times_incorrect__gte=models.F("times_correct")
    ).count()

    mastery_percent = 0

    if cards_reviewed > 0:
        mastery_percent = int(
            (known_cards / cards_reviewed) * 100
        )

    context = {
        "profile": profile,
        "xp_needed": xp_needed,
        "xp_percent": xp_percent,
        "user_achievements": user_achievements,
        "domain_progress": domain_progress,
        "cards_reviewed": cards_reviewed,
        "known_cards": known_cards,
        "practice_cards": practice_cards,
        "mastery_percent": mastery_percent,
    }

    return render(request, "dashboard.html", context)


@login_required
def choose_path(request):
    """
    Allows the logged-in user to choose their current certification path.
    """

    paths = CertificationPath.objects.filter(is_active=True)

    if request.method == "POST":
        path_id = request.POST.get("path_id")
        selected_path = CertificationPath.objects.get(id=path_id)

        profile = request.user.profile
        profile.selected_path = selected_path
        profile.save()

        return redirect("dashboard")

    context = {
        "paths": paths,
    }

    return render(request, "choose_path.html", context)
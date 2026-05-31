from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from achievements.models import UserAchievement


@login_required
def dashboard(request):
    """
    Displays the logged-in player's dashboard with:
    - level
    - XP progress
    - streak
    - unlocked achievements
    """

    profile = request.user.profile

    xp_needed = profile.level * 100
    xp_percent = int((profile.xp / xp_needed) * 100)

    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related("achievement")

    context = {
        "profile": profile,
        "xp_needed": xp_needed,
        "xp_percent": xp_percent,
        "user_achievements": user_achievements,
    }

    return render(request, "dashboard.html", context)
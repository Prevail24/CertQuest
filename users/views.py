from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Displays the logged-in player's dashboard with XP progress.
    """

    profile = request.user.profile
    xp_needed = profile.level * 100

    if xp_needed > 0:
        xp_percent = int((profile.xp / xp_needed) * 100)
    else:
        xp_percent = 0
    context = {
        "profile": profile,
        "xp_needed": xp_needed,
        "xp_percent": xp_percent,
    }

    return render(request, "dashboard.html", context)
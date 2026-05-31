from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import GameType


@login_required
def game_list(request):
    """
    Shows all active game types available to the logged-in player.
    """

    games = GameType.objects.filter(is_active=True)

    context = {
        "games": games,
    }

    return render(request, "games/game_list.html", context)
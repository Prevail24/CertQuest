"""
achievements/services.py

Handles achievement unlock logic.
"""

from .models import Achievement, UserAchievement


def award_first_response(user):
    """
    Awards the First Response achievement if the user
    has not already unlocked it.
    """

    achievement = Achievement.objects.filter(
        name="First Response"
    ).first()

    if not achievement:
        return False

    already_unlocked = UserAchievement.objects.filter(
        user=user,
        achievement=achievement
    ).exists()

    if already_unlocked:
        return False

    UserAchievement.objects.create(
        user=user,
        achievement=achievement
    )

    return True
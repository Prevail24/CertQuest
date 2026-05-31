
"""
progression/services.py

Handles CertQuest player progression logic:
- XP rewards
- Level-ups
- Daily streaks
"""

from datetime import timedelta

from django.utils import timezone


def add_xp(user, amount):
    """
    Adds XP to a user's profile and levels them up
    when they reach the required XP threshold.
    """

    profile = user.profile
    profile.xp += amount

    while profile.xp >= profile.level * 100:
        profile.xp -= profile.level * 100
        profile.level += 1

    profile.save()

    return profile.xp


def update_daily_streak(user):
    """
    Updates the user's daily streak after completing
    a correct Daily Quiz answer.
    """

    profile = user.profile
    today = timezone.localdate()

    if profile.last_streak_date == today:
        return profile.streak

    if profile.last_streak_date == today - timedelta(days=1):
        profile.streak += 1
    else:
        profile.streak = 1

    profile.last_streak_date = today
    profile.save()

    return profile.streak
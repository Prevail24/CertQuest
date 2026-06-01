"""
learning/services.py

Calculates learning progress across certification domains.
"""

from learning.models import Domain
from quests.models import UserAnswer


def get_domain_progress(user):
    """
    Returns progress stats for each domain in the user's selected path.
    """

    selected_path = user.profile.selected_path

    if not selected_path:
        return []

    domains = Domain.objects.filter(
        certification_path=selected_path
    )

    progress_data = []

    for domain in domains:
        answers = UserAnswer.objects.filter(
            user=user,
            question__domains=domain
        )

        total_answers = answers.count()
        correct_answers = answers.filter(is_correct=True).count()

        if total_answers > 0:
            percent = int((correct_answers / total_answers) * 100)
        else:
            percent = 0

        if percent >= 80:
            status = "🟢 Mastered"
        elif percent >= 50:
            status = "🟡 Improving"
        else:
            status = "🔴 Needs Review"
        boss_battle_unlocked = percent >= 80
        progress_data.append({
            "domain": domain,
            "total_answers": total_answers,
            "correct_answers": correct_answers,
            "percent": percent,
            "status": status,
            "boss_battle_unlocked": boss_battle_unlocked,
        })

    return progress_data
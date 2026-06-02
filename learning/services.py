"""
learning/services.py

Calculates learning progress across certification domains.
"""

from learning.models import Domain, UserFlashcard
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

def get_weak_flashcard_domains(user):
    """
    Finds domains where the user has more incorrect flashcard reviews
    than correct reviews.
    """

    selected_path = user.profile.selected_path

    if not selected_path:
        return []

    weak_domains = []

    domains = Domain.objects.filter(
        certification_path=selected_path
    )

    for domain in domains:
        user_flashcards = UserFlashcard.objects.filter(
            user=user,
            flashcard__domains=domain
        ).distinct()

        total_correct = 0
        total_incorrect = 0

        for user_flashcard in user_flashcards:
            total_correct += user_flashcard.times_correct
            total_incorrect += user_flashcard.times_incorrect

        if total_incorrect > total_correct:
            weak_domains.append({
                "domain": domain,
                "correct": total_correct,
                "incorrect": total_incorrect,
            })

    return weak_domains
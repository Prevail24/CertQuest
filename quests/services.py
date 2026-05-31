from quests.models import Question, UserAnswer
from progression.services import add_xp, update_daily_streak
from achievements.services import award_first_response

def submit_answer(user, question_id, answer):
    """
    Checks a user's answer, records it, and awards XP if correct.

    Args:
        user: The logged-in Django user.
        question_id: The ID of the question being answered.
        answer: The selected answer choice: A, B, C, or D.

    Returns:
        Dictionary containing correctness, XP gained, and explanation.
    """

    question = Question.objects.get(id=question_id)

    selected_answer = answer.strip().upper()
    correct_answer = question.correct_answer.strip().upper()

    is_correct = selected_answer == correct_answer

    UserAnswer.objects.create(
        user=user,
        question=question,
        answer=selected_answer,
        is_correct=is_correct,
    )

    xp_gained = 0

    if is_correct:
        xp_gained = question.xp_reward
        add_xp(user, xp_gained)
        update_daily_streak(user)
        award_first_response(user)

    return {
        "correct": is_correct,
        "xp_gained": xp_gained,
        "correct_answer": correct_answer,
        "explanation": question.explanation,
    }
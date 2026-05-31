from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from random import choice
from .models import Question
from .services import submit_answer


@login_required
def daily_quiz(request):
    """
    Displays a random cyber scenario question and processes answers.
    """

    selected_path = request.user.profile.selected_path

    if selected_path:
        questions = list(
            Question.objects.filter(
                certification_path=selected_path
            )
        )
    else:
        questions = list(Question.objects.all())

    if not questions:
        return render(
            request,
            "quests/no_questions.html"
        )

    question = choice(questions)

    if request.method == "POST":

        selected_answer = request.POST.get("answer")

        result = submit_answer(
            request.user,
            question.id,
            selected_answer
        )

        return render(
            request,
            "quests/result.html",
            {
                "question": question,
                "result": result
            }
        )

    return render(
        request,
        "quests/daily_quiz.html",
        {
            "question": question
        }
    )
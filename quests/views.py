from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from random import choice

from .models import Question, Scenario, ScenarioStep
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


@login_required
def scenario_detail(request, scenario_id):
    """
    Displays a multi-step cyber scenario.
    """

    scenario = get_object_or_404(Scenario, id=scenario_id)

    steps = ScenarioStep.objects.filter(
        scenario=scenario
    ).order_by("step_number")

    return render(
        request,
        "quests/scenario_detail.html",
        {
            "scenario": scenario,
            "steps": steps,
        }
    )

@login_required
def scenario_step(request, scenario_id):
    """
    Runs a scenario one step at a time using session data.
    """

    scenario = get_object_or_404(Scenario, id=scenario_id)

    steps = list(
        ScenarioStep.objects.filter(
            scenario=scenario
        ).order_by("step_number")
    )

    if not steps:
        return render(
            request,
            "quests/no_questions.html"
        )

    session_key = f"scenario_{scenario_id}_step"
    current_index = request.session.get(session_key, 0)

    if current_index >= len(steps):
        request.session[session_key] = 0

        return render(
            request,
            "quests/scenario_complete.html",
            {
                "scenario": scenario,
            }
        )

    current_step = steps[current_index]
    result = None

    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        correct_answer = current_step.correct_answer.upper()
        is_correct = selected_answer == correct_answer

        result = {
            "correct": is_correct,
            "correct_answer": correct_answer,
            "explanation": current_step.explanation,
        }

        if is_correct:
            request.session[session_key] = current_index + 1

    return render(
        request,
        "quests/scenario_step.html",
        {
            "scenario": scenario,
            "step": current_step,
            "result": result,
            "current_step_number": current_index + 1,
            "total_steps": len(steps),
        }
    )
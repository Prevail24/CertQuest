from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from random import choice, sample
from progression.services import add_xp
from .models import Question, Scenario, ScenarioStep, UserScenario, BossBattle, Question
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
        user_scenario, created = UserScenario.objects.get_or_create(
            user=request.user,
            scenario=scenario
        )

        xp_gained = 0

        if not user_scenario.completed:
            add_xp(request.user, scenario.xp_reward)

            user_scenario.completed = True
            user_scenario.completed_at = timezone.now()
            user_scenario.save()

            xp_gained = scenario.xp_reward

        request.session[session_key] = 0
        request.session.modified = True

        return render(
            request,
            "quests/scenario_complete.html",
            {
                "scenario": scenario,
                "xp_gained": xp_gained,
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
            request.session.modified = True

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

@login_required
def boss_battle_detail(request, boss_id):

    boss_battle = get_object_or_404(
        BossBattle,
        id=boss_id
    )

    return render(
        request,
        "quests/boss_battle_detail.html",
        {
            "boss_battle": boss_battle,
        }
    )

@login_required
def boss_battle_start(request, boss_id):

    boss_battle = get_object_or_404(
        BossBattle,
        id=boss_id
    )

    questions = list(
        Question.objects.filter(
            domains=boss_battle.domain
        ).distinct()
    )

    if len(questions) < boss_battle.questions_required:
        selected_questions = questions
    else:
        selected_questions = sample(
            questions,
            boss_battle.questions_required
        )

    request.session[
        f"boss_battle_{boss_id}_questions"
    ] = [q.id for q in selected_questions]

    request.session[
        f"boss_battle_{boss_id}_index"
    ] = 0

    request.session[
        f"boss_battle_{boss_id}_score"
    ] = 0

    request.session.modified = True

    return redirect(
        "boss_battle_question",
        boss_id=boss_id
    )

@login_required
def boss_battle_question(request, boss_id):

    boss_battle = get_object_or_404(
        BossBattle,
        id=boss_id
    )

    question_ids = request.session.get(
        f"boss_battle_{boss_id}_questions",
        []
    )

    current_index = request.session.get(
        f"boss_battle_{boss_id}_index",
        0
    )

    if current_index >= len(question_ids):
        return redirect(
            "boss_battle_complete",
            boss_id=boss_id
        )

    question = Question.objects.get(
        id=question_ids[current_index]
    )

    if request.method == "POST":

        selected_answer = request.POST.get(
            "answer"
        )

        correct_answer = question.correct_answer

        if selected_answer == correct_answer:

            score = request.session.get(
                f"boss_battle_{boss_id}_score",
                0
            )

            request.session[
                f"boss_battle_{boss_id}_score"
            ] = score + 1

        request.session[
            f"boss_battle_{boss_id}_index"
        ] = current_index + 1

        request.session.modified = True

        return redirect(
            "boss_battle_question",
            boss_id=boss_id
        )

    return render(
        request,
        "quests/boss_battle_question.html",
        {
            "boss_battle": boss_battle,
            "question": question,
            "current_question": current_index + 1,
            "total_questions": len(question_ids),
        }
    )

@login_required
def boss_battle_complete(request, boss_id):
    boss_battle = get_object_or_404(
        BossBattle,
        id=boss_id
    )

    question_ids = request.session.get(
        f"boss_battle_{boss_id}_questions",
        []
    )

    score = request.session.get(
        f"boss_battle_{boss_id}_score",
        0
    )

    total_questions = len(question_ids)

    percent = 0

    if total_questions > 0:
        percent = int((score / total_questions) * 100)

    passed = percent >= boss_battle.passing_score
    
    xp_gained = 0

    if passed:
        add_xp(request.user, boss_battle.xp_reward)
        xp_gained = boss_battle.xp_reward

    return render(
        request,
        "quests/boss_battle_complete.html",
        {
            "boss_battle": boss_battle,
            "score": score,
            "total_questions": total_questions,
            "percent": percent,
            "passed": passed,
            "xp_gained": xp_gained,
        }
    )
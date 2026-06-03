from django.db import models
from django.contrib.auth.models import User
from learning.models import CertificationPath, Domain 


class Quest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    cert_path = models.CharField(max_length=100)
    difficulty = models.IntegerField(default=1)

    xp_reward = models.IntegerField(default=25)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Question(models.Model):
    """
    Represents a single multiple-choice cyber scenario question.

    Questions are designed to feel like real-world IT, networking,
    or cybersecurity situations instead of plain textbook questions.
    """

    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    
    # Certification path this question belongs to
    certification_path = models.ForeignKey(
        CertificationPath,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    domains = models.ManyToManyField(
        Domain,
        blank=True
    )

    # Short title shown above the scenario
    title = models.CharField(max_length=255, default="Cyber Scenario")

    # Dramatic but realistic scenario text
    scenario = models.TextField(default="A security event has occurred.")

    # Actual question being asked
    text = models.TextField()

    # Multiple-choice options
    option_a = models.CharField(max_length=255, default="")
    option_b = models.CharField(max_length=255, default="")
    option_c = models.CharField(max_length=255, default="")
    option_d = models.CharField(max_length=255, default="")

    # Correct answer should be A, B, C, or D
    correct_answer = models.CharField(max_length=1)

    # Explanation shown after answering
    explanation = models.TextField(blank=True)

    xp_reward = models.IntegerField(default=10)

    def __str__(self):
        return self.title
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer = models.CharField(max_length=1)
    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

class Scenario(models.Model):
    """
    Multi-step cyber scenario.
    """

    title = models.CharField(max_length=255)

    certification_path = models.ForeignKey(
        CertificationPath,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    xp_reward = models.IntegerField(default=50)

    def __str__(self):
        return self.title
    
class ScenarioStep(models.Model):
    """
    Individual step within a scenario.
    """

    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE
    )

    step_number = models.IntegerField()

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=1)

    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.scenario.title} - Step {self.step_number}"
    
class UserScenario(models.Model):
    """
    Tracks scenario completion for each user.

    This prevents users from earning scenario XP repeatedly
    from the same scenario while still allowing replay for practice.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "scenario")

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title}"
    
class BossBattle(models.Model):

    title = models.CharField(max_length=255)

    certification_path = models.ForeignKey(
        CertificationPath,
        on_delete=models.CASCADE
    )
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE
    )
    description = models.CharField(
    max_length=255,
    blank=True,
    default=""
    )
    briefing = models.TextField(
        blank=True,
        default=""
    )
    xp_reward = models.IntegerField(
        default=100
    )
    is_active = models.BooleanField(
        default=True
    )

    questions_required = models.IntegerField(
    default=20
    )

    passing_score = models.IntegerField(
        default=80
    )

    def __str__(self):
        return self.title 
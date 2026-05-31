from django.db import models
from django.contrib.auth.models import User


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
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)

    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

    xp_reward = models.IntegerField(default=10)

    def __str__(self):
        return self.text[:50]


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
"""
achievements/models.py

Stores achievements users can unlock while progressing
through CertQuest certification paths.
"""

from django.contrib.auth.models import User
from django.db import models


class Achievement(models.Model):
    """
    Represents an achievement badge available in CertQuest.

    Achievements can be general or tied to a specific certificate path.
    """

    CERT_PATH_CHOICES = [
        ("general", "General"),
        ("network_plus", "Network+"),
        ("security_plus", "Security+"),
        ("a_plus", "A+"),
        ("ccna", "CCNA"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    cert_path = models.CharField(
        max_length=50,
        choices=CERT_PATH_CHOICES,
        default="general"
    )

    xp_bonus = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, default="🏅")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Connects a user to an achievement they have unlocked.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
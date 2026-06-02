"""
learning/models.py

Learning paths and certification tracks.
"""

from django.db import models


class CertificationPath(models.Model):
    """
    Represents a certification path available in CertQuest.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    # Visual theme name for this certification path
    theme_name = models.CharField(max_length=100, default="Default Theme")
    # Emoji/icon used throughout the UI
    icon = models.CharField(max_length=20, default="🎯")
    # Main accent color for this path
    primary_color = models.CharField(max_length=20, default="#38f2af")
    # Optional darker/supporting color
    secondary_color = models.CharField(max_length=20, default="#0b1020")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Domain(models.Model):
    """
    Represents a certification domain.
    Example:
    Security+ -> Threats
    Network+ -> Routing
    """

    certification_path = models.ForeignKey(
        CertificationPath,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.certification_path.name} - {self.name}"
    
class Flashcard(models.Model):
    """
    Study flashcards used for review and spaced repetition.
    """

    certification_path = models.ForeignKey(
        CertificationPath,
        on_delete=models.CASCADE
    )

    domains = models.ManyToManyField(
        Domain,
        blank=True
    )

    front = models.TextField()

    back = models.TextField()

    difficulty = models.IntegerField(
        default=1
    )

    xp_reward = models.IntegerField(
        default=2
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.front[:50]
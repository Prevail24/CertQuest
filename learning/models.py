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
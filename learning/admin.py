"""
learning/admin.py

Registers learning-related models so they can be managed
through the Django admin panel.
"""

from django.contrib import admin
from .models import CertificationPath, Domain, Flashcard

admin.site.register(Domain)
admin.site.register(CertificationPath)
@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):

    list_display = (
        "front",
        "certification_path",
        "difficulty",
        "xp_reward",
    )

    filter_horizontal = (
        "domains",
    )
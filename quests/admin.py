"""
quests/admin.py

Registers quest-related models.
"""

from django.contrib import admin

from .models import Quest, Question, UserAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Customizes how questions appear in Django Admin.

    filter_horizontal makes many-to-many fields easier to manage.
    """

    list_display = (
        "title",
        "certification_path",
        "correct_answer",
    )

    filter_horizontal = (
        "domains",
    )


admin.site.register(Quest)
admin.site.register(UserAnswer)
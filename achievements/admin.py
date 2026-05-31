"""
achievements/admin.py

Registers achievement models in Django admin.
"""

from django.contrib import admin
from .models import Achievement, UserAchievement


admin.site.register(Achievement)
admin.site.register(UserAchievement)